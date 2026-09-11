"""
Chat Repository — Data access for group chats, direct messaging, reactions, and expense embeds.
"""

import json
import time
from ..database import get_connection

def save_group_message(group_id, sender_id, sender_name, text, msg_type='text', attachment_url=None, expense_data=None, reply_to=None):
    conn = get_connection()
    cur = conn.cursor()
    msg_id = f"msg_{int(time.time() * 1000)}"
    exp_json = json.dumps(expense_data) if expense_data else None

    cur.execute('''
        INSERT INTO chat_messages (id, group_id, sender_id, sender_name, text, type, attachment_url, expense_data, reply_to, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (msg_id, group_id, sender_id, sender_name, text, msg_type, attachment_url, exp_json, reply_to))
    conn.commit()
    conn.close()

    return {
        "id": msg_id,
        "groupId": group_id,
        "senderId": sender_id,
        "senderName": sender_name,
        "text": text,
        "type": msg_type,
        "attachmentUrl": attachment_url,
        "expenseData": expense_data,
        "replyTo": reply_to,
        "reactions": {},
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def get_group_messages(group_id, limit=60):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, group_id, sender_id, sender_name, text, type, attachment_url, expense_data, reactions, reply_to, created_at
        FROM chat_messages
        WHERE group_id = ?
        ORDER BY created_at ASC
        LIMIT ?
    ''', (group_id, limit))
    rows = cur.fetchall()
    conn.close()

    messages = []
    for r in rows:
        exp_data = None
        if r['expense_data']:
            try:
                exp_data = json.loads(r['expense_data'])
            except Exception:
                pass
        reactions = {}
        if r['reactions']:
            try:
                reactions = json.loads(r['reactions'])
            except Exception:
                pass

        messages.append({
            "id": r['id'],
            "groupId": r['group_id'],
            "senderId": r['sender_id'],
            "senderName": r['sender_name'],
            "text": r['text'],
            "type": r['type'],
            "attachmentUrl": r['attachment_url'],
            "expenseData": exp_data,
            "reactions": reactions,
            "replyTo": r['reply_to'],
            "createdAt": r['created_at']
        })
    return messages

def add_reaction(msg_id, emoji, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT reactions FROM chat_messages WHERE id = ?', (msg_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    reactions = json.loads(row['reactions'] or '{}')
    users = reactions.get(emoji, [])
    if user_id in users:
        users.remove(user_id)
        if not users:
            del reactions[emoji]
        else:
            reactions[emoji] = users
    else:
        users.append(user_id)
        reactions[emoji] = users

    cur.execute('UPDATE chat_messages SET reactions = ? WHERE id = ?', (json.dumps(reactions), msg_id))
    conn.commit()
    conn.close()
    return reactions

def save_direct_message(conv_id, sender_id, sender_name, receiver_id, text, attachment_url=None):
    conn = get_connection()
    cur = conn.cursor()
    msg_id = f"dm_{int(time.time() * 1000)}"
    cur.execute('''
        INSERT INTO direct_messages (id, conv_id, sender_id, sender_name, receiver_id, text, attachment_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (msg_id, conv_id, sender_id, sender_name, receiver_id, text, attachment_url))
    conn.commit()
    conn.close()

    return {
        "id": msg_id,
        "convId": conv_id,
        "senderId": sender_id,
        "senderName": sender_name,
        "receiverId": receiver_id,
        "text": text,
        "attachmentUrl": attachment_url,
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def get_direct_messages(conv_id, limit=60):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, conv_id, sender_id, sender_name, receiver_id, text, attachment_url, created_at
        FROM direct_messages
        WHERE conv_id = ?
        ORDER BY created_at ASC
        LIMIT ?
    ''', (conv_id, limit))
    rows = cur.fetchall()
    conn.close()

    return [{
        "id": r['id'],
        "convId": r['conv_id'],
        "senderId": r['sender_id'],
        "senderName": r['sender_name'],
        "receiverId": r['receiver_id'],
        "text": r['text'],
        "attachmentUrl": r['attachment_url'],
        "createdAt": r['created_at']
    } for r in rows]
