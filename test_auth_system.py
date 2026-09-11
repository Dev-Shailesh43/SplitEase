import urllib.request
import urllib.error
import json

BASE_URL = "http://localhost:5000"

def post(endpoint, data, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get(endpoint, token=None):
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{endpoint}", headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("--- 1. Testing Default Persona Login (Admin Aman) ---")
login_res = post("/api/auth/login", {
    "email": "aman@campus.edu",
    "password": "admin123"
})
print("Login result:", login_res.get("status"), login_res.get("message"))
assert login_res.get("status") == "success"
assert "token" in login_res
assert login_res["user"]["email"] == "aman@campus.edu"
assert login_res["user"]["role"] == "admin"
token = login_res["token"]
print("PASS: Admin login works and returned session token.")

print("\n--- 2. Testing Session Validation with Token ---")
sess_res = get("/api/auth/session", token=token)
print("Session user:", sess_res.get("user", {}).get("displayName"))
assert sess_res.get("status") == "success"
assert sess_res["user"]["uid"] == "usr_aman"
print("PASS: Session token successfully verified.")

print("\n--- 3. Testing Wrong Password Rejection ---")
try:
    post("/api/auth/login", {
        "email": "aman@campus.edu",
        "password": "wrongpassword"
    })
    assert False, "Should have thrown 401"
except urllib.error.HTTPError as e:
    assert e.code == 401
    print("PASS: Incorrect password correctly rejected with 401.")

print("\n--- 4. Testing User Registration ---")
import time
test_email = f"newuser_{int(time.time())}@campus.edu"
reg_res = post("/api/auth/register", {
    "email": test_email,
    "password": "securepass123",
    "displayName": "Kavya Patel",
    "phoneNumber": "+91 91234 56789",
    "upiId": "kavya@okhdfc",
    "role": "member"
})
print("Registration status:", reg_res.get("status"), reg_res.get("message"))
assert reg_res.get("status") == "success"
assert "token" in reg_res
assert reg_res["user"]["displayName"] == "Kavya Patel"
new_token = reg_res["token"]
print("PASS: New user registered with hashed password and active session token.")

print("\n--- 5. Testing Login with Newly Registered User ---")
new_login = post("/api/auth/login", {
    "email": test_email,
    "password": "securepass123"
})
assert new_login.get("status") == "success"
print("PASS: Newly registered user can log in with their credentials.")

print("\n--- 6. Testing Duplicate Registration Rejection ---")
try:
    post("/api/auth/register", {
        "email": test_email,
        "password": "securepass123",
        "displayName": "Duplicate Kavya"
    })
    assert False, "Should have thrown 400"
except urllib.error.HTTPError as e:
    assert e.code == 400
    print("PASS: Duplicate registration correctly prevented with 400.")

print("\n--- 7. Testing Logout ---")
logout_res = post("/api/auth/logout", {"token": new_token})
assert logout_res.get("status") == "success"
try:
    get("/api/auth/session", token=new_token)
    assert False, "Should have thrown 401 after logout"
except urllib.error.HTTPError as e:
    assert e.code == 401
    print("PASS: Session invalidated upon logout.")

print("\nALL AUTH & SESSION BACKEND TESTS PASSED SUCCESSFULLY!")
