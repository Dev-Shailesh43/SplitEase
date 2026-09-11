"""
Auth Service — Profile management, session verification, and default user setup.
"""

from ..repositories.user_repo import get_user, save_user, list_users

DEFAULT_CAMPUS_PROFILES = [
    {
        "uid": "usr_aman",
        "displayName": "Aman Sharma",
        "username": "aman_304",
        "accountId": "CAMP-7492",
        "email": "aman@campus.edu",
        "phoneNumber": "+91 98765 43210",
        "upiId": "aman@okaxis",
        "secondaryUpiIds": ["aman@oksbi", "aman@paytm"],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "admin"
    },
    {
        "uid": "usr_rahul",
        "displayName": "Rahul Verma",
        "username": "rahul_v",
        "accountId": "CAMP-5831",
        "email": "rahul@campus.edu",
        "phoneNumber": "+91 98765 43211",
        "upiId": "rahul@oksbi",
        "secondaryUpiIds": ["rahul@paytm"],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "member"
    },
    {
        "uid": "usr_priya",
        "displayName": "Priya Patel",
        "username": "priya_p",
        "accountId": "CAMP-9104",
        "email": "priya@campus.edu",
        "phoneNumber": "+91 98765 43212",
        "upiId": "priya@okicici",
        "secondaryUpiIds": ["priya@gpay"],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "member"
    },
    {
        "uid": "usr_rohit",
        "displayName": "Rohit Sharma",
        "username": "rohit_s",
        "accountId": "CAMP-3329",
        "email": "rohit@campus.edu",
        "phoneNumber": "+91 98765 43213",
        "upiId": "rohit@paytm",
        "secondaryUpiIds": [],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "member"
    }
]

import hashlib
import uuid
from ..repositories.user_repo import (
    get_user, save_user, list_users,
    get_user_by_email, save_user_with_credentials,
    create_session, get_session, delete_session
)

def hash_password(password):
    salt = "splitease_fintech_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

SEED_CREDENTIALS = {
    "aman@campus.edu": ("admin123", "admin"),
    "rahul@campus.edu": ("rahul123", "member"),
    "priya@campus.edu": ("priya123", "member"),
    "rohit@campus.edu": ("rohit123", "member")
}

def ensure_seed_users():
    for u in DEFAULT_CAMPUS_PROFILES:
        email = u.get('email')
        existing_user, existing_hash = get_user_by_email(email)
        cred = SEED_CREDENTIALS.get(email, ("password123", u.get('role', 'member')))
        pwd_hash = hash_password(cred[0])
        u['role'] = cred[1]
        save_user_with_credentials(u['uid'], u, pwd_hash)

def get_or_create_profile(uid, fallback_data=None):
    profile = get_user(uid)
    if profile:
        return profile
    
    # Check default campus seed
    for u in DEFAULT_CAMPUS_PROFILES:
        if u['uid'] == uid:
            cred = SEED_CREDENTIALS.get(u.get('email'), ("password123", u.get('role', 'member')))
            pwd_hash = hash_password(cred[0])
            save_user_with_credentials(uid, u, pwd_hash)
            return u

    # Create new profile for authenticated user
    new_profile = {
        "uid": uid,
        "displayName": fallback_data.get('displayName', 'New Member') if fallback_data else 'New Member',
        "username": fallback_data.get('username', f"user_{uid[:6]}") if fallback_data else f"user_{uid[:6]}",
        "accountId": f"CAMP-{abs(hash(uid)) % 9000 + 1000}",
        "email": fallback_data.get('email', f"{uid[:8]}@campus.edu") if fallback_data else f"{uid[:8]}@campus.edu",
        "phoneNumber": fallback_data.get('phoneNumber', ''),
        "upiId": fallback_data.get('upiId', f"{uid[:6]}@upi"),
        "secondaryUpiIds": [],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "member"
    }
    save_user(uid, new_profile)
    return new_profile

def register_user(email, password, display_name, phone_number="", upi_id="", role="member"):
    if not email or not password:
        return False, "Email and password are required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    email = email.strip().lower()
    existing_user, _ = get_user_by_email(email)
    if existing_user:
        return False, "An account with this email address already exists"

    uid = f"usr_{uuid.uuid4().hex[:8]}"
    username = email.split('@')[0]
    generated_upi = upi_id.strip() if upi_id and upi_id.strip() else f"{username}@okcampus"
    
    profile = {
        "uid": uid,
        "displayName": display_name.strip() if display_name else username,
        "username": username,
        "accountId": f"CAMP-{abs(hash(uid)) % 9000 + 1000}",
        "email": email,
        "phoneNumber": phone_number.strip(),
        "upiId": generated_upi,
        "secondaryUpiIds": [],
        "customQrImage": None,
        "currency": "INR",
        "language": "English",
        "role": "admin" if role == "admin" else "member"
    }

    pwd_hash = hash_password(password)
    save_user_with_credentials(uid, profile, pwd_hash)

    token = f"sess_{uuid.uuid4().hex}"
    create_session(token, uid)

    return True, {"user": profile, "token": token}

def login_user(email, password):
    if not email or not password:
        return False, "Email and password are required"

    email = email.strip().lower()
    ensure_seed_users() # Ensure default personas exist with valid credentials

    user, pwd_hash = get_user_by_email(email)
    if not user or not pwd_hash:
        return False, "Invalid email or password"

    input_hash = hash_password(password)
    if input_hash != pwd_hash:
        return False, "Invalid email or password"

    token = f"sess_{uuid.uuid4().hex}"
    create_session(token, user['uid'])

    return True, {"user": user, "token": token}

def validate_session(token):
    if not token:
        return None
    uid = get_session(token)
    if not uid:
        return None
    return get_user(uid)

def logout_user(token):
    if token:
        delete_session(token)
    return True
