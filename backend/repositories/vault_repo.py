"""
Vault Repository — Data access for stored documents, invoices, and bill proofs.
"""

import time
from ..database import get_connection

def save_vault_file(group_id, filename, category, uploaded_by, file_data):
    conn = get_connection()
    cur = conn.cursor()
    file_id = f"vlt_{int(time.time() * 1000)}"
    cur.execute('''
        INSERT INTO vault_files (id, group_id, filename, category, uploaded_by, file_data, created_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (file_id, group_id, filename, category, uploaded_by, file_data))
    conn.commit()
    conn.close()

    return {
        "id": file_id,
        "groupId": group_id,
        "filename": filename,
        "category": category,
        "uploadedBy": uploaded_by,
        "createdAt": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def list_vault_files(group_id=None):
    conn = get_connection()
    cur = conn.cursor()
    if group_id:
        cur.execute('''
            SELECT id, group_id, filename, category, uploaded_by, created_at
            FROM vault_files
            WHERE group_id = ?
            ORDER BY created_at DESC
        ''', (group_id,))
    else:
        cur.execute('''
            SELECT id, group_id, filename, category, uploaded_by, created_at
            FROM vault_files
            ORDER BY created_at DESC
        ''')
    rows = cur.fetchall()
    conn.close()

    return [{
        "id": r['id'],
        "groupId": r['group_id'],
        "filename": r['filename'],
        "category": r['category'],
        "uploadedBy": r['uploaded_by'],
        "createdAt": r['created_at']
    } for r in rows]

def get_vault_file(file_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, group_id, filename, category, uploaded_by, file_data, created_at FROM vault_files WHERE id = ?', (file_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def delete_vault_file(file_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM vault_files WHERE id = ?', (file_id,))
    conn.commit()
    conn.close()
    return True
