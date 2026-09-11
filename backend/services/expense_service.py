"""
Expense Service — Debt graph minimization algorithm, multi-payer split calculation, and balance consistency engine.
"""

def recalculate_group_balances(group):
    """
    Computes mathematically consistent net balances for all members in a group.
    Net Balance = Total Amount Contributed - Total Share Consumed
    """
    members = group.get('members', [])
    expenses = group.get('expenses', [])

    balances = {}
    for m in members:
        balances[m['uid']] = {
            "uid": m['uid'],
            "name": m.get('displayName', 'Member'),
            "totalPaid": 0.0,
            "totalShare": 0.0,
            "netBalance": 0.0
        }

    for exp in expenses:
        amount = float(exp.get('amount', 0))
        
        # 1. Who paid? (Single payer or Multi-payer)
        payers = exp.get('payers')
        if payers and isinstance(payers, list) and len(payers) > 0:
            for p in payers:
                p_uid = p.get('uid')
                p_amt = float(p.get('amount', 0))
                if p_uid in balances:
                    balances[p_uid]['totalPaid'] += p_amt
        else:
            paid_by_uid = exp.get('paidBy', {}).get('uid') if isinstance(exp.get('paidBy'), dict) else exp.get('paidBy')
            if paid_by_uid in balances:
                balances[paid_by_uid]['totalPaid'] += amount

        # 2. Who owes? (Splits)
        splits = exp.get('splits', [])
        if splits:
            for s in splits:
                s_uid = s.get('uid')
                s_amt = float(s.get('amount', 0))
                if s_uid in balances:
                    balances[s_uid]['totalShare'] += s_amt
        elif len(members) > 0:
            # Default equal split fallback
            share = amount / len(members)
            for m in members:
                balances[m['uid']]['totalShare'] += share

    # Compute net balance
    for uid in balances:
        balances[uid]['netBalance'] = round(balances[uid]['totalPaid'] - balances[uid]['totalShare'], 2)

    return balances

def minimize_debts(balances, members):
    """
    Greedy Debt Minimization Algorithm (Max Flow / Bipartite matching).
    Reduces total bilateral transactions down to minimum direct transfers.
    """
    member_map = {m['uid']: m for m in members}

    debtors = []   # (amount_owed, uid)
    creditors = [] # (amount_owed_to, uid)

    for uid, b in balances.items():
        net = round(b['netBalance'], 2)
        if net < -0.01:
            debtors.append([-net, uid])
        elif net > 0.01:
            creditors.append([net, uid])

    debtors.sort(key=lambda x: x[0], reverse=True)
    creditors.sort(key=lambda x: x[0], reverse=True)

    transactions = []
    d_idx = 0
    c_idx = 0

    while d_idx < len(debtors) and c_idx < len(creditors):
        debtor = debtors[d_idx]
        creditor = creditors[c_idx]

        settle_amt = round(min(debtor[0], creditor[0]), 2)
        if settle_amt > 0.01:
            transactions.append({
                "from": member_map.get(debtor[1], {"uid": debtor[1], "displayName": "Debtor"}),
                "to": member_map.get(creditor[1], {"uid": creditor[1], "displayName": "Creditor"}),
                "amount": settle_amt
            })

        debtor[0] -= settle_amt
        creditor[0] -= settle_amt

        if debtor[0] <= 0.01:
            d_idx += 1
        if creditor[0] <= 0.01:
            c_idx += 1

    return transactions
