"""
Auth Controller — Profile, Settings, Friendships, and Account Lifecycle.
"""

from ..repositories.user_repo import get_user, save_user, delete_user, get_friends, add_friend, list_users
from ..services.auth_service import (
    get_or_create_profile, register_user, login_user, validate_session, logout_user
)
from ..repositories.notification_repo import log_audit
from ..middleware.error_handler import make_success_response, make_error_response

def handle_register(body):
    email = body.get('email')
    password = body.get('password')
    display_name = body.get('displayName')
    phone_number = body.get('phoneNumber', '')
    upi_id = body.get('upiId', '')
    role = body.get('role', 'member')

    ok, result = register_user(email, password, display_name, phone_number, upi_id, role)
    if not ok:
        return make_error_response(result, 400)
    
    log_audit("register", f"User {result['user']['displayName']} ({email}) registered")
    return make_success_response({
        "status": "success",
        "user": result['user'],
        "token": result['token'],
        "message": "Account registered successfully"
    }, 201)

def handle_login(body):
    email = body.get('email')
    password = body.get('password')

    ok, result = login_user(email, password)
    if not ok:
        return make_error_response(result, 401)

    log_audit("login", f"User {result['user']['displayName']} logged in")
    return make_success_response({
        "status": "success",
        "user": result['user'],
        "token": result['token'],
        "message": "Signed in successfully"
    })

def handle_validate_session(token):
    if not token:
        return make_error_response("Session token missing", 401)
    user = validate_session(token)
    if not user:
        return make_error_response("Invalid or expired session", 401)
    return make_success_response({"status": "success", "user": user})

def handle_logout(body):
    token = body.get('token')
    if token:
        logout_user(token)
    return make_success_response({"status": "success", "message": "Logged out successfully"})

def handle_get_profile(params):
    uid = params.get('uid', [None])[0]
    if not uid:
        return make_error_response("Missing uid parameter", 400)
    profile = get_or_create_profile(uid)
    return make_success_response({"profile": profile})

def handle_save_profile(body):
    uid = body.get('uid')
    if not uid:
        return make_error_response("Missing uid in request body", 400)
    saved = save_user(uid, body)
    log_audit("update_profile", f"User {uid} updated profile settings")
    return make_success_response({"profile": saved, "message": "Profile updated successfully"})

def handle_delete_account(body):
    uid = body.get('uid')
    if not uid:
        return make_error_response("Missing uid", 400)
    delete_user(uid)
    log_audit("delete_account", f"User {uid} deleted their account")
    return make_success_response({"message": "Account successfully deleted"})

def handle_get_friends(params):
    uid = params.get('uid', [None])[0]
    if not uid:
        return make_error_response("Missing uid", 400)
    friends = get_friends(uid)
    all_users = list_users()
    suggested = [u for u in all_users if u.get('uid') != uid and not any(f.get('uid') == u.get('uid') for f in friends)]
    return make_success_response({"friends": friends, "suggested": suggested[:10]})

def handle_add_friend(body):
    uid = body.get('uid')
    friend_id = body.get('friendId')
    if not uid or not friend_id:
        return make_error_response("Missing uid or friendId", 400)
    add_friend(uid, friend_id)
    log_audit("add_friend", f"User {uid} added friend {friend_id}")
    return make_success_response({"message": "Friend added successfully"})
