"""
User Repository — Data access for profiles, credentials, and friendships.
"""

import json
from ..database import get_connection

def get_user(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json FROM user_profiles WHERE uid = ?', (uid,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row['data_json'])
    return None

def save_user(uid, profile_dict):
    conn = get_connection()
    cur = conn.cursor()
    email = profile_dict.get('email', '')
    display_name = profile_dict.get('displayName', '')
    cur.execute('''
        INSERT INTO user_profiles (uid, email, display_name, data_json, updated_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(uid) DO UPDATE SET
            email = excluded.email,
            display_name = excluded.display_name,
            data_json = excluded.data_json,
            updated_at = CURRENT_TIMESTAMP
    ''', (uid, email, display_name, json.dumps(profile_dict)))
    conn.commit()
    conn.close()
    return profile_dict

def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json FROM user_profiles ORDER BY updated_at DESC')
    rows = cur.fetchall()
    conn.close()
    users = []
    for r in rows:
        try:
            users.append(json.loads(r['data_json']))
        except Exception:
            pass
    return users

def delete_user(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM user_profiles WHERE uid = ?', (uid,))
    cur.execute('DELETE FROM friends WHERE user_id = ? OR friend_id = ?', (uid, uid))
    cur.execute('DELETE FROM notifications WHERE user_id = ?', (uid,))
    conn.commit()
    conn.close()
    return True

def get_friends(uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT friend_id FROM friends WHERE user_id = ?', (uid,))
    rows = cur.fetchall()
    conn.close()
    friend_ids = [r['friend_id'] for r in rows]
    friends = []
    for fid in friend_ids:
        u = get_user(fid)
        if u:
            friends.append(u)
    return friends

def add_friend(uid, friend_id):
    if uid == friend_id:
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT OR IGNORE INTO friends (user_id, friend_id)
        VALUES (?, ?), (?, ?)
    ''', (uid, friend_id, friend_id, uid))
    conn.commit()
    conn.close()
    return True

def get_user_by_email(email):
    if not email:
        return None, None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json, password_hash FROM user_profiles WHERE LOWER(email) = LOWER(?)', (email.strip(),))
    row = cur.fetchone()
    conn.close()
    if row:
        try:
            return json.loads(row['data_json']), row['password_hash']
        except Exception:
            return None, None
    return None, None

def save_user_with_credentials(uid, profile_dict, password_hash=None):
    conn = get_connection()
    cur = conn.cursor()
    email = profile_dict.get('email', '')
    display_name = profile_dict.get('displayName', '')
    if password_hash:
        cur.execute('''
            INSERT INTO user_profiles (uid, email, display_name, password_hash, data_json, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(uid) DO UPDATE SET
                email = excluded.email,
                display_name = excluded.display_name,
                password_hash = excluded.password_hash,
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
        ''', (uid, email, display_name, password_hash, json.dumps(profile_dict)))
    else:
        cur.execute('''
            INSERT INTO user_profiles (uid, email, display_name, data_json, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(uid) DO UPDATE SET
                email = excluded.email,
                display_name = excluded.display_name,
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
        ''', (uid, email, display_name, json.dumps(profile_dict)))
    conn.commit()
    conn.close()
    return profile_dict

def create_session(token, uid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO auth_sessions (token, uid) VALUES (?, ?)', (token, uid))
    conn.commit()
    conn.close()
    return True

def get_session(token):
    if not token:
        return None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT uid FROM auth_sessions WHERE token = ?', (token,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row['uid']
    return None

def delete_session(token):
    if not token:
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM auth_sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()
    return True
