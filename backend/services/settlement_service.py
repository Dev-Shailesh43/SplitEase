"""
Settlement Service — Manages peer-to-peer UPI claims, verification workflows, and debt clearing.
"""

import time
from .expense_service import recalculate_group_balances, minimize_debts
from ..repositories.notification_repo import create_notification, log_activity

def create_payment_claim(group, from_user, to_user, amount, upi_ref, screenshot_url=None):
    claim_id = f"claim_{int(time.time() * 1000)}"
    claim = {
        "id": claim_id,
        "fromUid": from_user.get('uid'),
        "fromName": from_user.get('displayName'),
        "toUid": to_user.get('uid'),
        "toName": to_user.get('displayName'),
        "amount": float(amount),
        "upiRef": upi_ref,
        "paymentProof": screenshot_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending"
    }

    pending_claims = group.get('pendingClaims', [])
    pending_claims.append(claim)
    group['pendingClaims'] = pending_claims

    # Notify payee
    create_notification(
        user_id=to_user.get('uid'),
        title="Payment Claim Received",
        message=f"{from_user.get('displayName')} claimed a payment of ₹{amount} (Ref: {upi_ref}). Click to review and confirm.",
        notif_type="payment",
        ref_id=claim_id
    )

    log_activity(
        group_id=group.get('groupId'),
        user_id=from_user.get('uid'),
        user_name=from_user.get('displayName'),
        action="claimed_payment",
        details=f"Paid ₹{amount} to {to_user.get('displayName')} (Ref: {upi_ref})"
    )

    return claim

def confirm_payment_claim(group, claim_id, confirmed_by_uid):
    pending_claims = group.get('pendingClaims', [])
    matched_claim = None

    for c in pending_claims:
        cid = c.get('id') or c.get('claimId')
        to_uid = c.get('toUid') or (c.get('payee', {}).get('uid')) or (c.get('to', {}).get('uid'))
        if cid == claim_id and (to_uid == confirmed_by_uid or group.get('createdBy') == confirmed_by_uid or confirmed_by_uid in group.get('admins', [])):
            matched_claim = c
            break

    if not matched_claim:
        return False, "Claim not found or you are not authorized to confirm it."

    pending_claims.remove(matched_claim)
    group['pendingClaims'] = pending_claims

    # Convert claim into an official group settlement expense
    settlement_expense = {
        "id": f"settle_{int(time.time() * 1000)}",
        "title": f"Settlement: {matched_claim.get('fromName') or matched_claim.get('payer', {}).get('displayName', 'Member')} -> {matched_claim.get('toName') or matched_claim.get('payee', {}).get('displayName', 'Payee')}",
        "category": "Settlement",
        "icon": "💸",
        "amount": float(matched_claim.get('amount')),
        "paidBy": {"uid": matched_claim.get('fromUid') or matched_claim.get('payer', {}).get('uid'), "displayName": matched_claim.get('fromName') or matched_claim.get('payer', {}).get('displayName')},
        "splits": [{"uid": matched_claim.get('toUid') or matched_claim.get('payee', {}).get('uid'), "amount": float(matched_claim.get('amount'))}],
        "billImage": matched_claim.get('paymentProof') or matched_claim.get('proofUrl'),
        "comments": [{"author": "System", "text": f"UPI Settlement confirmed (Ref: {matched_claim.get('upiRef') or matched_claim.get('utr', 'N/A')})", "timestamp": "Just now"}],
        "timeline": [f"Settlement confirmed by {matched_claim.get('toName') or 'Payee'}"],
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses = group.get('expenses', [])
    expenses.append(settlement_expense)
    group['expenses'] = expenses

    # Log activity & notify payer
    payer_uid = matched_claim.get('fromUid') or matched_claim.get('payer', {}).get('uid')
    if payer_uid:
        create_notification(
            user_id=payer_uid,
            title="Payment Claim Confirmed",
            message=f"{matched_claim.get('toName') or 'Payee'} verified and accepted your payment of ₹{matched_claim.get('amount')}.",
            notif_type="success",
            ref_id=settlement_expense['id']
        )

    log_activity(
        group_id=group.get('groupId'),
        user_id=confirmed_by_uid,
        user_name=matched_claim.get('toName') or 'Payee',
        action="confirmed_claim",
        details=f"Cleared debt of ₹{matched_claim.get('amount')} from {matched_claim.get('fromName') or 'Member'}"
    )

    return True, settlement_expense

def decline_payment_claim(group, claim_id, declined_by_uid, reason="Payment not received in account"):
    pending_claims = group.get('pendingClaims', [])
    matched_claim = None

    for c in pending_claims:
        cid = c.get('id') or c.get('claimId')
        to_uid = c.get('toUid') or (c.get('payee', {}).get('uid')) or (c.get('to', {}).get('uid'))
        if cid == claim_id and (to_uid == declined_by_uid or group.get('createdBy') == declined_by_uid or declined_by_uid in group.get('admins', [])):
            matched_claim = c
            break

    if not matched_claim:
        return False, "Claim not found or you are not authorized to decline it."

    pending_claims.remove(matched_claim)
    group['pendingClaims'] = pending_claims

    # Notify payer that claim was declined
    payer_uid = matched_claim.get('fromUid') or matched_claim.get('payer', {}).get('uid')
    to_name = matched_claim.get('toName') or matched_claim.get('payee', {}).get('displayName', 'Payee')
    if payer_uid:
        create_notification(
            user_id=payer_uid,
            title="Payment Claim Declined",
            message=f"{to_name} declined your payment claim of ₹{matched_claim.get('amount')}. Reason: {reason}",
            notif_type="warning",
            ref_id=claim_id
        )

    log_activity(
        group_id=group.get('groupId'),
        user_id=declined_by_uid,
        user_name=to_name,
        action="declined_claim",
        details=f"Declined claim of ₹{matched_claim.get('amount')} from {matched_claim.get('fromName') or 'Member'} ({reason})"
    )

    return True, matched_claim

def direct_cash_settlement(group, from_user, to_user, amount, note="Direct Settlement"):
    settlement_expense = {
        "id": f"settle_direct_{int(time.time() * 1000)}",
        "title": f"Settlement: {from_user.get('displayName')} -> {to_user.get('displayName')}",
        "category": "Settlement",
        "icon": "💵",
        "amount": float(amount),
        "paidBy": {"uid": from_user.get('uid'), "displayName": from_user.get('displayName')},
        "splits": [{"uid": to_user.get('uid'), "amount": float(amount)}],
        "billImage": None,
        "comments": [{"author": "System", "text": f"Direct settlement recorded ({note})", "timestamp": "Just now"}],
        "timeline": [f"Settlement of ₹{amount} recorded by {to_user.get('displayName')}"],
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }

    expenses = group.get('expenses', [])
    expenses.insert(0, settlement_expense)
    group['expenses'] = expenses

    create_notification(
        user_id=from_user.get('uid'),
        title="Direct Settlement Cleared",
        message=f"{to_user.get('displayName')} recorded a direct settlement of ₹{amount}. Your debt is cleared.",
        notif_type="success",
        ref_id=settlement_expense['id']
    )

    log_activity(
        group_id=group.get('groupId'),
        user_id=to_user.get('uid'),
        user_name=to_user.get('displayName'),
        action="direct_settlement",
        details=f"Recorded direct payment of ₹{amount} from {from_user.get('displayName')}"
    )

    return True, settlement_expense

