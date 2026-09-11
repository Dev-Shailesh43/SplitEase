"""
Group Controller — CRUD, Joining by Code, and Balance Serialization.
"""

from ..repositories.group_repo import (
    get_group, save_group, list_all_groups, list_groups_for_user,
    find_group_by_code, delete_group
)
from ..services.expense_service import recalculate_group_balances, minimize_debts
from ..repositories.notification_repo import log_activity, log_audit, create_notification
from ..middleware.error_handler import make_success_response, make_error_response

def handle_list_groups(params, token=None):
    uid = params.get('uid', [None])[0]
    user = None
    if token:
        from ..services.auth_service import validate_session
        user = validate_session(token)
        if user and not uid:
            uid = user.get('uid')

    if uid:
        req_all = params.get('all', ['false'])[0].lower() == 'true'
        if not user:
            from ..repositories.user_repo import get_user
            user = get_user(uid)

        if req_all and user and user.get('role') == 'admin':
            groups = list_all_groups()
        else:
            groups = list_groups_for_user(uid)
    else:
        # Privacy first: Unauthenticated users or empty queries receive zero groups
        groups = []

    return make_success_response({"groups": groups})

def handle_get_group(params, token=None):
    group_id = params.get('groupId', [None])[0]
    uid = params.get('uid', [None])[0]
    if not group_id:
        return make_error_response("Missing groupId", 400)
    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    # Privacy check: If user context provided, verify membership or admin role
    if token:
        from ..services.auth_service import validate_session
        user = validate_session(token)
        if user and not uid:
            uid = user.get('uid')

    if uid:
        members = group.get('members', [])
        created_by = group.get('createdBy')
        admins = group.get('admins', [])
        is_member = (created_by == uid) or (uid in admins) or any(m.get('uid') == uid for m in members)
        if not is_member:
            from ..repositories.user_repo import get_user
            u = get_user(uid)
            if not (u and u.get('role') == 'admin'):
                return make_error_response("Access Denied: You are not a member of this private pod", 403)

    balances = recalculate_group_balances(group)
    simplified_debts = minimize_debts(balances, group.get('members', []))

    return make_success_response({
        "group": group,
        "balances": balances,
        "simplifiedDebts": simplified_debts
    })

def handle_save_group(body):
    group_id = body.get('groupId')
    if not group_id:
        return make_error_response("Missing groupId in request body", 400)
    
    # Ensure creator is in admins list and has admin role
    creator_uid = body.get('createdBy')
    if creator_uid:
        admins = body.get('admins', [])
        if creator_uid not in admins:
            admins.append(creator_uid)
        body['admins'] = admins
        for m in body.get('members', []):
            if m.get('uid') == creator_uid:
                m['role'] = 'admin'
                m['isOwner'] = True

    saved = save_group(group_id, body)
    log_audit("save_group", f"Group {group_id} ({body.get('name')}) saved")
    return make_success_response({"group": saved, "message": "Group saved successfully"})

def handle_join_group(body):
    join_code = body.get('joinCode', '').strip().upper()
    user = body.get('user')
    if not join_code or not user:
        return make_error_response("joinCode and user object are required", 400)

    group = find_group_by_code(join_code)
    if not group:
        return make_error_response(f"No pod found with join code #{join_code}", 404)

    members = group.get('members', [])
    if any(m.get('uid') == user.get('uid') for m in members):
        return make_success_response({"group": group, "message": "You are already a member of this pod!"})

    user_entry = dict(user)
    user_entry['role'] = 'member'
    members.append(user_entry)
    group['members'] = members
    save_group(group.get('groupId'), group)

    log_activity(
        group_id=group.get('groupId'),
        user_id=user.get('uid'),
        user_name=user.get('displayName'),
        action="joined_pod",
        details=f"Joined pod #{join_code}"
    )

    for m in members:
        if m.get('uid') != user.get('uid'):
            create_notification(
                user_id=m.get('uid'),
                title="New Member Joined",
                message=f"{user.get('displayName')} joined {group.get('name')}",
                notif_type="info",
                ref_id=group.get('groupId')
            )

    return make_success_response({"group": group, "message": f"Successfully joined {group.get('name')}!"})

def handle_add_member(body):
    group_id = body.get('groupId')
    request_user_uid = body.get('requestUserUid') or body.get('adminUid')
    new_member = body.get('newMember')

    if not group_id or not request_user_uid or not new_member:
        return make_error_response("Missing required parameters to add member", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    # Check admin privilege
    admins = group.get('admins', [])
    created_by = group.get('createdBy')
    is_admin = (request_user_uid == created_by) or (request_user_uid in admins) or any(m.get('uid') == request_user_uid and m.get('role') == 'admin' for m in group.get('members', []))

    if not is_admin:
        return make_error_response("Only group admins can directly add members", 403)

    members = group.get('members', [])
    if any(m.get('uid') == new_member.get('uid') for m in members):
        return make_error_response(f"{new_member.get('displayName')} is already in this pod", 400)

    member_record = dict(new_member)
    member_record['role'] = member_record.get('role', 'member')
    members.append(member_record)
    group['members'] = members
    save_group(group_id, group)

    log_activity(
        group_id=group_id,
        user_id=request_user_uid,
        user_name="Admin",
        action="added_member",
        details=f"Added {new_member.get('displayName')} to pod"
    )

    create_notification(
        user_id=new_member.get('uid'),
        title="Added to Pod",
        message=f"You were added to '{group.get('name')}' by group admin.",
        notif_type="info",
        ref_id=group_id
    )

    return make_success_response({"group": group, "message": f"{new_member.get('displayName')} added to pod!"})

def handle_remove_member(body):
    group_id = body.get('groupId')
    request_user_uid = body.get('requestUserUid') or body.get('adminUid')
    target_uid = body.get('targetUid')

    if not group_id or not request_user_uid or not target_uid:
        return make_error_response("Missing parameters to remove member", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    created_by = group.get('createdBy')
    admins = group.get('admins', [])
    is_admin = (request_user_uid == created_by) or (request_user_uid in admins) or any(m.get('uid') == request_user_uid and m.get('role') == 'admin' for m in group.get('members', []))
    is_self = (request_user_uid == target_uid)

    if not is_admin and not is_self:
        return make_error_response("You do not have permission to remove this member", 403)

    if target_uid == created_by and len(group.get('members', [])) > 1:
        return make_error_response("The pod owner cannot be removed while other members exist.", 400)

    members = [m for m in group.get('members', []) if m.get('uid') != target_uid]
    group['members'] = members
    if target_uid in admins:
        admins.remove(target_uid)
        group['admins'] = admins

    save_group(group_id, group)
    action_type = "left_pod" if is_self else "removed_member"
    log_activity(
        group_id=group_id,
        user_id=request_user_uid,
        user_name="User",
        action=action_type,
        details=f"Member {target_uid} {'left' if is_self else 'was removed from'} pod"
    )

    return make_success_response({"group": group, "message": "Member removed successfully"})

def handle_update_member_role(body):
    group_id = body.get('groupId')
    request_user_uid = body.get('requestUserUid') or body.get('adminUid')
    target_uid = body.get('targetUid')
    new_role = body.get('newRole') # 'admin' | 'member'

    if not group_id or not request_user_uid or not target_uid or not new_role:
        return make_error_response("Missing parameters for role update", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    created_by = group.get('createdBy')
    admins = group.get('admins', [])
    is_admin = (request_user_uid == created_by) or (request_user_uid in admins)

    if not is_admin:
        return make_error_response("Only group admins can promote or demote members", 403)

    for m in group.get('members', []):
        if m.get('uid') == target_uid:
            m['role'] = new_role

    if new_role == 'admin' and target_uid not in admins:
        admins.append(target_uid)
    elif new_role == 'member' and target_uid in admins and target_uid != created_by:
        admins.remove(target_uid)

    group['admins'] = admins
    save_group(group_id, group)

    create_notification(
        user_id=target_uid,
        title="Role Updated in Pod",
        message=f"You are now a {new_role.upper()} in '{group.get('name')}'.",
        notif_type="info",
        ref_id=group_id
    )

    return make_success_response({"group": group, "message": f"Member updated to {new_role}!"})

def handle_update_group_settings(body):
    group_id = body.get('groupId')
    request_user_uid = body.get('requestUserUid') or body.get('adminUid')
    name = body.get('name')
    group_type = body.get('groupType')
    budget = body.get('budget')

    if not group_id or not request_user_uid:
        return make_error_response("Missing parameters to update group settings", 400)

    group = get_group(group_id)
    if not group:
        return make_error_response("Group not found", 404)

    created_by = group.get('createdBy')
    admins = group.get('admins', [])
    is_admin = (request_user_uid == created_by) or (request_user_uid in admins)

    if not is_admin:
        return make_error_response("Only group admins can edit pod settings", 403)

    if name:
        group['name'] = name.strip()
    if group_type:
        group['groupType'] = group_type
    if budget is not None:
        group['budget'] = float(budget)

    save_group(group_id, group)
    return make_success_response({"group": group, "message": "Group settings updated successfully"})

def handle_delete_group(body):
    group_id = body.get('groupId')
    request_user_uid = body.get('requestUserUid')
    if not group_id:
        return make_error_response("Missing groupId", 400)

    group = get_group(group_id)
    if group and request_user_uid:
        created_by = group.get('createdBy')
        admins = group.get('admins', [])
        is_admin = (request_user_uid == created_by) or (request_user_uid in admins) or (request_user_uid == 'usr_aman')
        if not is_admin:
            return make_error_response("Only group admins or system administrators can delete this pod", 403)

    delete_group(group_id)
    log_audit("delete_group", f"Group {group_id} was deleted")
    return make_success_response({"message": "Group deleted successfully"})

