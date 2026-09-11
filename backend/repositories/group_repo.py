"""
Group Repository — Data access for groups, shared ledgers, and settlements.
"""

import json
from ..database import get_connection

def get_group(group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json FROM groups WHERE id = ?', (group_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row['data_json'])
    return None

def save_group(group_id, group_dict):
    conn = get_connection()
    cur = conn.cursor()
    name = group_dict.get('name', 'Pod')
    join_code = group_dict.get('joinCode', '')
    group_type = group_dict.get('groupType', 'Friends')
    cur.execute('''
        INSERT INTO groups (id, name, join_code, group_type, data_json, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            join_code = excluded.join_code,
            group_type = excluded.group_type,
            data_json = excluded.data_json,
            updated_at = CURRENT_TIMESTAMP
    ''', (group_id, name, join_code, group_type, json.dumps(group_dict)))
    conn.commit()
    conn.close()
    return group_dict

def list_all_groups():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json FROM groups ORDER BY updated_at DESC')
    rows = cur.fetchall()
    conn.close()
    groups = []
    for r in rows:
        try:
            groups.append(json.loads(r['data_json']))
        except Exception:
            pass
    return groups

def list_groups_for_user(uid):
    all_g = list_all_groups()
    user_groups = []
    for g in all_g:
        members = g.get('members', [])
        created_by = g.get('createdBy')
        admins = g.get('admins', [])
        if created_by == uid or uid in admins or any(m.get('uid') == uid for m in members):
            user_groups.append(g)
    return user_groups

def find_group_by_code(join_code):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT data_json FROM groups WHERE join_code = ?', (join_code.strip().upper(),))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row['data_json'])
    return None

def delete_group(group_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM groups WHERE id = ?', (group_id,))
    cur.execute('DELETE FROM chat_messages WHERE group_id = ?', (group_id,))
    cur.execute('DELETE FROM vault_files WHERE group_id = ?', (group_id,))
    conn.commit()
    conn.close()
    return True

def ensure_seed_groups():
    existing = list_all_groups()
    if not existing:
        from ..services.auth_service import DEFAULT_CAMPUS_PROFILES
        seed_groups = [
            {
                "groupId": "pod_hackathon",
                "name": "Hackathon Team Alpha",
                "groupType": "College",
                "tag": "HT",
                "joinCode": "HK-9824",
                "createdBy": "usr_aman",
                "members": DEFAULT_CAMPUS_PROFILES,
                "expenses": [
                    {
                        "id": "exp_1",
                        "title": "Cloud GPU & AI Credits",
                        "category": "Tech",
                        "icon": "💻",
                        "amount": 3200,
                        "paidBy": DEFAULT_CAMPUS_PROFILES[0],
                        "billImage": None,
                        "comments": [{"author": "Rahul", "text": "Used for fine-tuning our model!", "timestamp": "Yesterday"}],
                        "timeline": ["Created by Aman", "Split equally among 4 members"],
                        "createdAt": "2026-09-10T12:00:00.000Z",
                        "splits": [{"uid": u["uid"], "amount": 800} for u in DEFAULT_CAMPUS_PROFILES]
                    },
                    {
                        "id": "exp_2",
                        "title": "Midnight Red Bull & Pizza",
                        "category": "Food",
                        "icon": "🍕",
                        "amount": 1800,
                        "paidBy": DEFAULT_CAMPUS_PROFILES[2],
                        "billImage": None,
                        "comments": [{"author": "Aman", "text": "Tasted great thanks Priya", "timestamp": "12 hours ago"}],
                        "timeline": ["Created by Priya", "Split equally among 4 members"],
                        "createdAt": "2026-09-11T00:30:00.000Z",
                        "splits": [{"uid": u["uid"], "amount": 450} for u in DEFAULT_CAMPUS_PROFILES]
                    }
                ],
                "pendingClaims": [
                    {
                        "id": "claim_1",
                        "fromUid": "usr_rahul",
                        "fromName": "Rahul Verma",
                        "toUid": "usr_aman",
                        "toName": "Aman Sharma",
                        "amount": 550,
                        "upiRef": "UPI-REF-9028471",
                        "paymentProof": None,
                        "status": "PENDING_CONFIRMATION",
                        "timestamp": "2026-09-11 11:30:00"
                    }
                ],
                "settlements": []
            },
            {
                "groupId": "pod_goa_trip",
                "name": "Goa Trip 2026",
                "groupType": "Trip",
                "tag": "GT",
                "joinCode": "GOA-2026",
                "createdBy": "usr_aman",
                "budget": 60000,
                "itinerary": [
                    {"day": "Day 1", "date": "15 Oct", "title": "Arrival & Beach Villa Check-in", "place": "Calangute, North Goa"},
                    {"day": "Day 2", "date": "16 Oct", "title": "Scuba Diving & Watersports", "place": "Grand Island"},
                    {"day": "Day 3", "date": "17 Oct", "title": "Sunset Cruise & Seafood Feast", "place": "Panjim Riverfront"}
                ],
                "members": DEFAULT_CAMPUS_PROFILES,
                "expenses": [
                    {
                        "id": "exp_goa_1",
                        "title": "Boutique Sea-Facing Villa (3 Nights)",
                        "category": "Hotels",
                        "icon": "🏨",
                        "amount": 18000,
                        "paidBy": DEFAULT_CAMPUS_PROFILES[0],
                        "billImage": None,
                        "comments": [{"author": "Aman", "text": "Confirmed booking reference #VIL-9921", "timestamp": "2 days ago"}],
                        "timeline": ["Created by Aman", "Split among 4 members"],
                        "createdAt": "2026-09-09T15:00:00.000Z",
                        "splits": [{"uid": u["uid"], "amount": 4500} for u in DEFAULT_CAMPUS_PROFILES]
                    }
                ],
                "pendingClaims": [],
                "settlements": []
            },
            {
                "groupId": "pod_flat402",
                "name": "Flat 402 Roommates",
                "groupType": "Flat",
                "tag": "F4",
                "joinCode": "FLAT-402",
                "createdBy": "usr_rahul",
                "members": DEFAULT_CAMPUS_PROFILES,
                "expenses": [
                    {
                        "id": "exp_flat_1",
                        "title": "Airtel Fiber Gigabit Internet",
                        "category": "Utilities",
                        "icon": "📶",
                        "amount": 1499,
                        "paidBy": DEFAULT_CAMPUS_PROFILES[1],
                        "billImage": None,
                        "comments": [],
                        "timeline": ["Created by Rahul", "Split among 4 roommates"],
                        "createdAt": "2026-09-01T10:00:00.000Z",
                        "splits": [{"uid": u["uid"], "amount": 374.75} for u in DEFAULT_CAMPUS_PROFILES]
                    }
                ],
                "pendingClaims": [],
                "settlements": []
            }
        ]
        for g in seed_groups:
            save_group(g["groupId"], g)

