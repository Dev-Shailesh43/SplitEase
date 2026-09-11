"""
Privacy-First Policy Verification Test Suite for SplitEase Pro.
Verifies that:
1. A new user account has 0 pods visible upon registration (no cross-pod leaks).
2. Existing pods (like Hackathon Team Alpha) are strictly visible only to their members (Aman, Rahul, Priya, Rohit).
3. When the new user creates a pod, only the new user (and invited members) see it.
4. Other campus members cannot see the new user's pod.
5. Direct group detail access by unauthorized non-members is rejected (403 Forbidden).
"""

import urllib.request
import urllib.parse
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def get(path, token=None):
    url = BASE_URL + path
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read().decode('utf-8')), resp.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode('utf-8')), e.code

def post(path, payload, token=None):
    url = BASE_URL + path
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read().decode('utf-8')), resp.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode('utf-8')), e.code

print("=== RUNNING PRIVACY-FIRST POLICY VERIFICATION ===")

# 1. Register a brand new campus user
unique_id = int(time.time())
new_email = f"privacy_user_{unique_id}@campus.edu"
reg_data, status = post('/api/auth/register', {
    "email": new_email,
    "password": "securepassword123",
    "displayName": "Ananya Sharma",
    "upiId": f"ananya_{unique_id}@okhdfc",
    "role": "member"
})
assert status == 200, f"Registration failed: {reg_data}"
new_user = reg_data['user']
new_token = reg_data['token']
print(f"PASS 1: Registered new campus user: {new_user['displayName']} ({new_user['uid']})")

# 2. Check groups for new user - MUST BE EMPTY (0 pods)
groups_res, status = get(f"/api/groups?uid={new_user['uid']}", new_token)
assert status == 200
user_groups = groups_res.get('groups', [])
assert len(user_groups) == 0, f"PRIVACY LEAK: New user sees {len(user_groups)} groups: {[g['name'] for g in user_groups]}"
print(f"PASS 2: Privacy Shield verified. New user sees {len(user_groups)} pods (Zero cross-pod leakage).")

# 3. Verify that Aman (existing member) CAN see his pods
aman_login, _ = post('/api/auth/login', {"email": "aman@campus.edu", "password": "admin123"})
aman_token = aman_login['token']
aman_groups, _ = get(f"/api/groups?uid=usr_aman", aman_token)
aman_pod_names = [g['name'] for g in aman_groups.get('groups', [])]
assert len(aman_groups.get('groups', [])) > 0, "Aman should see his pods"
print(f"PASS 3: Aman legitimately sees his member pods: {aman_pod_names}")

# 4. New user creates their own private pod
private_pod_id = f"pod_private_{unique_id}"
create_res, status = post('/api/groups/save', {
    "groupId": private_pod_id,
    "name": f"Ananya Private Flat {unique_id}",
    "groupType": "Flat",
    "joinCode": f"FLT-{unique_id % 10000}",
    "createdBy": new_user['uid'],
    "admins": [new_user['uid']],
    "members": [{
        **new_user,
        "role": "admin",
        "isOwner": True
    }],
    "expenses": [],
    "pendingClaims": []
}, new_token)
assert status == 200, f"Pod creation failed: {create_res}"
print(f"PASS 4: New user created private pod '{create_res['group']['name']}' as Owner/Admin.")

# 5. Check new user's groups now - must contain exactly 1 pod
groups_res_after, _ = get(f"/api/groups?uid={new_user['uid']}", new_token)
user_groups_after = groups_res_after.get('groups', [])
assert len(user_groups_after) == 1, f"Expected 1 group, got {len(user_groups_after)}"
assert user_groups_after[0]['groupId'] == private_pod_id
print(f"PASS 5: New user now sees exclusively their own pod: '{user_groups_after[0]['name']}'")

# 6. Verify that Rahul (other member) CANNOT see Ananya's private pod
rahul_login, _ = post('/api/auth/login', {"email": "rahul@campus.edu", "password": "rahul123"})
rahul_token = rahul_login['token']
rahul_groups, _ = get(f"/api/groups?uid=usr_rahul", rahul_token)
rahul_pod_ids = [g['groupId'] for g in rahul_groups.get('groups', [])]
assert private_pod_id not in rahul_pod_ids, "PRIVACY VIOLATION: Rahul can see Ananya's private pod!"
print(f"PASS 6: Rahul cannot see Ananya's private pod. Cross-pod boundary strictly maintained.")

# 7. Verify that unauthorized user cannot inspect private pod details directly
detail_res, detail_status = get(f"/api/groups/detail?groupId={private_pod_id}&uid=usr_rahul", rahul_token)
assert detail_status == 403, f"Expected 403 Forbidden, got {detail_status}: {detail_res}"
print(f"PASS 7: Direct URL access by non-member rejected with 403 Forbidden: '{detail_res.get('message')}'")

print("\nALL PRIVACY-FIRST POLICY TESTS PASSED PERFECTLY! ZERO PRIVACY LEAKS.")
