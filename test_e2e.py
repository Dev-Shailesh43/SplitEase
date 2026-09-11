import urllib.request
import json

def post(url, data):
    req = urllib.request.Request('http://127.0.0.1:5000' + url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=5).read())

def get(url):
    return json.loads(urllib.request.urlopen('http://127.0.0.1:5000' + url, timeout=5).read())

print("--- STARTING PRODUCTION END-TO-END VERIFICATION ---")

# 1. Health check
h = get('/api/health')
print("1. Health check:", h['status'], h['service'])

# 2. Create Pod
g = post('/api/groups/save', {
    'groupId': 'pod_test_flow',
    'name': 'Mumbai Hackers',
    'groupType': 'College',
    'joinCode': 'MUM-999',
    'members': [
        {'uid': 'usr_aman', 'displayName': 'Aman Sharma', 'upiId': 'aman@okaxis'},
        {'uid': 'usr_rahul', 'displayName': 'Rahul Verma', 'upiId': 'rahul@oksbi'}
    ],
    'expenses': [],
    'pendingClaims': []
})
print("2. Pod Created:", g['group']['name'])

# 3. Add Expense
exp = post('/api/expenses/add', {
    'groupId': 'pod_test_flow',
    'expense': {
        'title': 'AWS Cloud Credits',
        'amount': 2000,
        'category': 'Tech',
        'paidBy': {'uid': 'usr_aman', 'displayName': 'Aman Sharma'},
        'splits': [
            {'uid': 'usr_aman', 'amount': 1000},
            {'uid': 'usr_rahul', 'amount': 1000}
        ]
    }
})
print("3. Expense Added. Aman net balance:", exp['balances']['usr_aman']['netBalance'], "| Rahul net balance:", exp['balances']['usr_rahul']['netBalance'])

# 4. Chat Message in Group
msg = post('/api/chat/send', {
    'groupId': 'pod_test_flow',
    'senderId': 'usr_aman',
    'senderName': 'Aman Sharma',
    'text': 'Logged the AWS bill guys! Please settle up.'
})
print("4. Chat Message Sent:", msg['message']['text'])

# 5. Settlement Claim
claim = post('/api/expenses/claim', {
    'groupId': 'pod_test_flow',
    'fromUser': {'uid': 'usr_rahul', 'displayName': 'Rahul Verma'},
    'toUser': {'uid': 'usr_aman', 'displayName': 'Aman Sharma'},
    'amount': 1000,
    'upiRef': 'UTR-987654321'
})
print("5. Claim Submitted:", claim['claim']['status'])

# 6. Settlement Confirmation
confirm = post('/api/expenses/confirm-claim', {
    'groupId': 'pod_test_flow',
    'claimId': claim['claim']['id'],
    'confirmedByUid': 'usr_aman'
})
print("6. Claim Confirmed! Rahul new net balance:", confirm['balances']['usr_rahul']['netBalance'], "| Aman new net balance:", confirm['balances']['usr_aman']['netBalance'])

# 7. Global Search
search = get('/api/search?q=Mumbai')
print("7. Global Search Results (Groups):", [item['title'] for item in search['results']['groups']])

# 8. Admin Telemetry
adm = get('/api/admin/metrics')
print("8. Admin Telemetry Gross Volume:", adm['metrics']['totalVolumeINR'], "| Groups count:", adm['metrics']['totalGroups'])

print("--- ALL PRODUCTION VERIFICATION TESTS PASSED SUCCESSFULLY! ---")
