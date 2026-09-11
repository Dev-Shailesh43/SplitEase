"""
SplitEase Pro — Database Schema & Connection Management
Supports SQLite persistence and transactional consistency for financial and chat operations.
"""

import sqlite3
import json
from .config import DB_FILE

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 1. User Profiles
    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            uid TEXT PRIMARY KEY,
            email TEXT,
            display_name TEXT,
            data_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        cur.execute("ALTER TABLE user_profiles ADD COLUMN email TEXT")
    except Exception:
        pass
    try:
        cur.execute("ALTER TABLE user_profiles ADD COLUMN display_name TEXT")
    except Exception:
        pass
    try:
        cur.execute("ALTER TABLE user_profiles ADD COLUMN password_hash TEXT")
    except Exception:
        pass

    # 1b. User Auth Sessions
    cur.execute('''
        CREATE TABLE IF NOT EXISTS auth_sessions (
            token TEXT PRIMARY KEY,
            uid TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP
        )
    ''')

    # 2. Groups / Pods
    cur.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            join_code TEXT,
            group_type TEXT DEFAULT 'Friends',
            data_json TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    try:
        cur.execute("ALTER TABLE groups ADD COLUMN group_type TEXT DEFAULT 'Friends'")
    except Exception:
        pass
    try:
        cur.execute("ALTER TABLE groups ADD COLUMN join_code TEXT")
    except Exception:
        pass

    # 3. Group Chat Messages
    cur.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id TEXT PRIMARY KEY,
            group_id TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            sender_name TEXT,
            text TEXT,
            type TEXT DEFAULT 'text',
            attachment_url TEXT,
            expense_data TEXT,
            reactions TEXT DEFAULT '{}',
            reply_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. 1-on-1 Direct Messages
    cur.execute('''
        CREATE TABLE IF NOT EXISTS direct_messages (
            id TEXT PRIMARY KEY,
            conv_id TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            sender_name TEXT,
            receiver_id TEXT NOT NULL,
            text TEXT,
            attachment_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Vault Documents & Receipts
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vault_files (
            id TEXT PRIMARY KEY,
            group_id TEXT,
            filename TEXT,
            category TEXT,
            uploaded_by TEXT,
            file_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 6. User Notifications
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'info',
            ref_id TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 7. Activity Log
    cur.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id TEXT,
            user_id TEXT,
            user_name TEXT,
            action TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 8. Friends Relationships
    cur.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user_id TEXT NOT NULL,
            friend_id TEXT NOT NULL,
            status TEXT DEFAULT 'accepted',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, friend_id)
        )
    ''')

    # 9. System Audit Log
    cur.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
