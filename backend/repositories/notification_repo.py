"""
Notification & Activity Repository — In-app alerts, activity feeds, and audit trail.
"""

import time
import uuid
from ..database import get_connection

def create_notification(user_id, title, message, notif_type='info', ref_id=None):
    conn = get_connection()
    cur = conn.cursor()
    notif_id = f"notif_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}"
    cur.execute('''
        INSERT INTO notifications (id, user_id, title, message, type, ref_id, is_read, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, CURRENT_TIMESTAMP)
    ''', (notif_id, user_id, title, message, notif_type, ref_id))
    conn.commit()
    conn.close()

    return {
        "id": notif_id,
        "userId": user_id,
        "title": title,
        "message": message,
        "type": notif_type,
        "refId": ref_id,
        "isRead": False,
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def get_notifications(user_id, limit=40):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, user_id, title, message, type, ref_id, is_read, created_at
        FROM notifications
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (user_id, limit))
    rows = cur.fetchall()
    conn.close()

    return [{
        "id": r['id'],
        "userId": r['user_id'],
        "title": r['title'],
        "message": r['message'],
        "type": r['type'],
        "refId": r['ref_id'],
        "isRead": bool(r['is_read']),
        "createdAt": r['created_at']
    } for r in rows]

def mark_as_read(notif_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notifications SET is_read = 1 WHERE id = ?', (notif_id,))
    conn.commit()
    conn.close()
    return True

def mark_all_as_read(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True

def log_activity(group_id, user_id, user_name, action, details=''):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO activity_log (group_id, user_id, user_name, action, details, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (group_id, user_id, user_name, action, details))
    conn.commit()
    conn.close()

def get_activities(group_id=None, limit=50):
    conn = get_connection()
    cur = conn.cursor()
    if group_id:
        cur.execute('''
            SELECT id, group_id, user_id, user_name, action, details, created_at
            FROM activity_log
            WHERE group_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (group_id, limit))
    else:
        cur.execute('''
            SELECT id, group_id, user_id, user_name, action, details, created_at
            FROM activity_log
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
    rows = cur.fetchall()
    conn.close()

    return [{
        "id": r['id'],
        "groupId": r['group_id'],
        "userId": r['user_id'],
        "userName": r['user_name'],
        "action": r['action'],
        "details": r['details'],
        "createdAt": r['created_at']
    } for r in rows]

def log_audit(action, details=''):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO audit_log (action, details, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)', (action, details))
    conn.commit()
    conn.close()

def get_audit_logs(limit=40):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, action, details, timestamp FROM audit_log ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()

    return [{
        "id": r['id'],
        "action": r['action'],
        "details": r['details'],
        "timestamp": r['timestamp']
    } for r in rows]
