import urllib.request
import json
import time

BASE_URL = "http://localhost:5000"

def post(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get(endpoint):
    with urllib.request.urlopen(f"{BASE_URL}{endpoint}") as resp:
        return json.loads(resp.read().decode('utf-8'))

print("--- 1. Testing GET /api/admin/users ---")
users_res = get("/api/admin/users")
print("Admin users count:", len(users_res.get("users", [])))
assert "users" in users_res
print("PASS: Admin users listing works.")

print("\n--- 2. Testing Pod Creation with Creator as Admin ---")
test_pod_id = f"test_pod_{int(time.time())}"
creator_uid = "usr_creator_001"
creator_user = {
    "uid": creator_uid,
    "displayName": "Alex Creator",
    "email": "alex@campus.edu",
    "role": "admin",
    "isOwner": True
}
new_pod = {
    "groupId": test_pod_id,
    "name": "Hackathon Admin Pod",
    "tag": "HAP",
    "groupType": "Project",
    "joinCode": "TEST99",
    "createdBy": creator_uid,
    "admins": [creator_uid],
    "members": [creator_user],
    "expenses": [],
    "pendingClaims": []
}
save_res = post("/api/groups/save", new_pod)
assert save_res.get("status") == "success"
print("PASS: Pod saved with creator as admin.")

print("\n--- 3. Testing Adding a Member to Pod ---")
new_member = {
    "uid": "usr_member_002",
    "displayName": "Bella Tester",
    "email": "bella@campus.edu",
    "upiId": "bella@okhdfc"
}
add_res = post("/api/groups/members/add", {
    "groupId": test_pod_id,
    "adminUid": creator_uid,
    "newMember": new_member
})
print("Add member res:", add_res.get("status"))
assert add_res.get("status") == "success"
print("PASS: Group admin successfully added member.")

print("\n--- 4. Testing Promoting Member to Co-Admin ---")
role_res = post("/api/groups/members/role", {
    "groupId": test_pod_id,
    "adminUid": creator_uid,
    "targetUid": "usr_member_002",
    "newRole": "admin"
})
print("Update role res:", role_res.get("status"))
assert role_res.get("status") == "success"
print("PASS: Member promoted to co-admin.")

print("\n--- 5. Testing Updating Pod Settings ---")
settings_res = post("/api/groups/settings/update", {
    "groupId": test_pod_id,
    "adminUid": creator_uid,
    "name": "Hackathon Admin Pod VIP",
    "tag": "VIP"
})
print("Settings update res:", settings_res.get("status"))
assert settings_res.get("status") == "success"
print("PASS: Group admin updated pod settings.")

print("\n--- 6. Testing Direct Cash Settlement ---")
settle_res = post("/api/expenses/settle-direct", {
    "groupId": test_pod_id,
    "fromUser": new_member,
    "toUser": creator_user,
    "amount": 250.0,
    "note": "Settled via Cash in Canteen"
})
print("Direct settlement res:", settle_res.get("status"))
assert settle_res.get("status") == "success"
print("PASS: Direct cash settlement recorded.")

print("\n--- 7. Testing Submitting and Declining a Payment Claim ---" )
claim_payload = {
    "groupId": test_pod_id,
    "claim": {
        "claimId": f"claim_{int(time.time())}",
        "payer": new_member,
        "payee": creator_user,
        "amount": 120.0,
        "mode": "UPI / GPay",
        "utr": "UTR123456789",
        "note": "Paid for printouts",
        "createdAt": "2026-09-11T14:00:00Z"
    }
}
claim_res = post("/api/expenses/claim", claim_payload)
assert claim_res.get("status") == "success"
claim_id = claim_res.get("claim", {}).get("id") or claim_payload["claim"]["claimId"]

decline_res = post("/api/expenses/decline-claim", {
    "groupId": test_pod_id,
    "claimId": claim_id,
    "declinedByUid": creator_uid,
    "reason": "Payment not received in bank account yet"
})
print("Decline claim res:", decline_res.get("status"))
assert decline_res.get("status") == "success"
print("PASS: Payee successfully declined payment claim with reason.")

print("\n--- 8. Testing System Admin Role Update ---")
admin_role_res = post("/api/admin/users/role", {
    "targetUid": "usr_member_002",
    "newRole": "admin"
})
print("Admin set user role res:", admin_role_res.get("status"))
assert admin_role_res.get("status") == "success"
print("PASS: System admin updated global user role.")

print("\n--- 9. Testing Removing a Member from Pod ---")
remove_res = post("/api/groups/members/remove", {
    "groupId": test_pod_id,
    "adminUid": creator_uid,
    "targetUid": "usr_member_002"
})
print("Remove member res:", remove_res.get("status"))
assert remove_res.get("status") == "success"
print("PASS: Group admin removed member from pod.")

print("\nALL BACKEND API VERIFICATIONS PASSED SUCCESSFULLY!")
