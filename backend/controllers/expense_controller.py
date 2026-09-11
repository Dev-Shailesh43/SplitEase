"""
Expense Controller — Expense Logging, Deletion, Settlement Claims and Verification.
"""

import time
from ..repositories.group_repo import get_group, save_group
from ..services.expense_service import recalculate_group_balances, minimize_debts
from ..services.settlement_service import create_payment_claim, confirm_payment_claim, decline_payment_claim, direct_cash_settlement
from ..repositories.notification_repo import log_activity, log_audit, create_notification
from ..middleware.error_handler import make_success_response, make_error_response

def handle_add_expense(body):
    group_id = body.get('groupId')
    expense = body.get('expense')
    if not group_id or not expense:
        return make_error_response("Missing groupId or expense data", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    if not expense.get('id'):
        expense['id'] = f"exp_{int(time.time() * 1000)}"
    if not expense.get('createdAt'):
        expense['createdAt'] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    expenses = group.get('expenses', [])
    expenses.insert(0, expense)
    group['expenses'] = expenses

    save_group(group_id, group)

    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    paid_by_name = expense.get('paidBy', {}).get('displayName', 'Member') if isinstance(expense.get('paidBy'), dict) else 'Member'
    log_activity(
        group_id=group_id,
        user_id=expense.get('paidBy', {}).get('uid', 'usr') if isinstance(expense.get('paidBy'), dict) else 'usr',
        user_name=paid_by_name,
        action="added_expense",
        details=f"Added '{expense.get('title')}' for ₹{expense.get('amount')}"
    )

    # Notify participants
    for s in expense.get('splits', []):
        s_uid = s.get('uid')
        if s_uid != (expense.get('paidBy', {}).get('uid') if isinstance(expense.get('paidBy'), dict) else None):
            create_notification(
                user_id=s_uid,
                title="New Expense Added",
                message=f"{paid_by_name} added '{expense.get('title')}' (your share: ₹{s.get('amount')})",
                notif_type="expense",
                ref_id=expense['id']
            )

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts,
        "expense": expense,
        "message": "Expense logged and balances recalculated"
    })

def handle_delete_expense(body):
    group_id = body.get('groupId')
    expense_id = body.get('expenseId')
    if not group_id or not expense_id:
        return make_error_response("Missing groupId or expenseId", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    expenses = group.get('expenses', [])
    group['expenses'] = [e for e in expenses if e.get('id') != expense_id]
    save_group(group_id, group)

    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    log_audit("delete_expense", f"Expense {expense_id} deleted from group {group_id}")

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts,
        "message": "Expense deleted successfully"
    })

def handle_claim_payment(body):
    group_id = body.get('groupId')
    claim_dict = body.get('claim', {})
    from_user = body.get('fromUser') or claim_dict.get('payer')
    to_user = body.get('toUser') or claim_dict.get('payee')
    amount = body.get('amount') or claim_dict.get('amount')
    upi_ref = body.get('upiRef') or claim_dict.get('utr') or 'UPI-MANUAL'
    screenshot_url = body.get('screenshot') or claim_dict.get('proofUrl')

    if not group_id or not from_user or not to_user or not amount:
        return make_error_response("Missing required settlement claim parameters", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    claim = create_payment_claim(group, from_user, to_user, amount, upi_ref, screenshot_url)
    save_group(group_id, group)

    return make_success_response({"claim": claim, "group": group, "message": "Payment claim submitted for payee confirmation"})

def handle_confirm_claim(body):
    group_id = body.get('groupId')
    claim_id = body.get('claimId')
    confirmed_by_uid = body.get('confirmedByUid')

    if not group_id or not claim_id or not confirmed_by_uid:
        return make_error_response("Missing required confirmation parameters", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    ok, result = confirm_payment_claim(group, claim_id, confirmed_by_uid)
    if not ok:
        return make_error_response(result, 400)

    save_group(group_id, group)
    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts,
        "message": "Payment verified and debt settled!"
    })

def handle_decline_claim(body):
    group_id = body.get('groupId')
    claim_id = body.get('claimId')
    declined_by_uid = body.get('declinedByUid')
    reason = body.get('reason', 'Payment not received in account')

    if not group_id or not claim_id or not declined_by_uid:
        return make_error_response("Missing required decline parameters", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    ok, result = decline_payment_claim(group, claim_id, declined_by_uid, reason)
    if not ok:
        return make_error_response(result, 400)

    save_group(group_id, group)
    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts,
        "message": f"Payment claim declined ({reason})"
    })

def handle_direct_settlement(body):
    group_id = body.get('groupId')
    from_user = body.get('fromUser')
    to_user = body.get('toUser')
    amount = body.get('amount')
    note = body.get('note', 'Direct Cash Payment')

    if not group_id or not from_user or not to_user or not amount:
        return make_error_response("Missing required direct settlement parameters", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    ok, result = direct_cash_settlement(group, from_user, to_user, amount, note)
    if not ok:
        return make_error_response("Failed to record settlement", 400)

    save_group(group_id, group)
    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts,
        "message": f"Direct settlement of ₹{amount} recorded!"
    })

