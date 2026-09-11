"""
Chat Controller — Group real-time chat, 1-on-1 messaging, expense embeds, and emoji reactions.
"""

from ..repositories.chat_repo import (
    save_group_message, get_group_messages, add_reaction,
    save_direct_message, get_direct_messages
)
from ..repositories.notification_repo import create_notification
from ..middleware.error_handler import make_success_response, make_error_response

def handle_get_group_messages(params):
    group_id = params.get('groupId', [None])[0]
    if not group_id:
        return make_error_response("Missing groupId", 400)
    messages = get_group_messages(group_id)
    return make_success_response({"messages": messages})

def handle_send_group_message(body):
    group_id = body.get('groupId')
    sender_id = body.get('senderId')
    sender_name = body.get('senderName', 'Member')
    text = body.get('text', '')
    msg_type = body.get('type', 'text')
    attachment_url = body.get('attachmentUrl')
    expense_data = body.get('expenseData')
    reply_to = body.get('replyTo')

    if not group_id or not sender_id or (not text and not attachment_url and not expense_data):
        return make_error_response("groupId, senderId, and message content are required", 400)

    saved_msg = save_group_message(
        group_id=group_id,
        sender_id=sender_id,
        sender_name=sender_name,
        text=text,
        msg_type=msg_type,
        attachment_url=attachment_url,
        expense_data=expense_data,
        reply_to=reply_to
    )

    return make_success_response({"message": saved_msg})

def handle_react_message(body):
    msg_id = body.get('messageId')
    emoji = body.get('emoji')
    user_id = body.get('userId')
    if not msg_id or not emoji or not user_id:
        return make_error_response("messageId, emoji, and userId are required", 400)

    updated_reactions = add_reaction(msg_id, emoji, user_id)
    return make_success_response({"reactions": updated_reactions})

def handle_get_direct_messages(params):
    conv_id = params.get('convId', [None])[0]
    if not conv_id:
        # Generate deterministic convId from userA and userB if provided
        user_a = params.get('userA', [None])[0]
        user_b = params.get('userB', [None])[0]
        if user_a and user_b:
            conv_id = f"conv_{'_'.join(sorted([user_a, user_b]))}"
        else:
            return make_error_response("Missing convId or (userA, userB)", 400)

    messages = get_direct_messages(conv_id)
    return make_success_response({"convId": conv_id, "messages": messages})

def handle_send_direct_message(body):
    sender_id = body.get('senderId')
    sender_name = body.get('senderName', 'User')
    receiver_id = body.get('receiverId')
    text = body.get('text', '')
    attachment_url = body.get('attachmentUrl')

    if not sender_id or not receiver_id or not text:
        return make_error_response("senderId, receiverId, and text are required", 400)

    conv_id = f"conv_{'_'.join(sorted([sender_id, receiver_id]))}"
    saved_msg = save_direct_message(
        conv_id=conv_id,
        sender_id=sender_id,
        sender_name=sender_name,
        receiver_id=receiver_id,
        text=text,
        attachment_url=attachment_url
    )

    create_notification(
        user_id=receiver_id,
        title=f"Message from {sender_name}",
        message=text[:80],
        notif_type="chat",
        ref_id=conv_id
    )

    return make_success_response({"message": saved_msg, "convId": conv_id})
