"""
SplitEase Pro — Enterprise Modular FinTech Server
Clean modular dispatcher routing requests to Controllers, Services, and Repositories.
"""

import http.server
import socketserver
import json
import os
import urllib.parse

from backend.config import PORT, GEMINI_MODEL
from backend.database import init_db
from backend.services.auth_service import ensure_seed_users
from backend.controllers import (
    auth_controller,
    group_controller,
    expense_controller,
    chat_controller,
    vault_controller,
    ai_controller,
    admin_controller
)

class SplitEaseRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        # Health Endpoint
        if path == '/api/health':
            self.send_json_response({
                "status": "healthy",
                "service": "SplitEase Pro Layered FinTech Engine",
                "version": "3.0.0",
                "architecture": "Layered MVC (Controllers, Services, Repositories)",
                "ai_engine": f"Google Gemini ({GEMINI_MODEL})",
                "database": "SQLite Local + Firebase Cloud Sync",
                "firebase_project": "splitease-9b53d",
                "uptime": "active"
            })
            return

        # Groups & Ledgers
        if path == '/api/groups':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip() if 'Bearer ' in auth_header else params.get('token', [None])[0]
            res, code = group_controller.handle_list_groups(params, token)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/detail':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip() if 'Bearer ' in auth_header else params.get('token', [None])[0]
            res, code = group_controller.handle_get_group(params, token)
            self.send_json_response(res, code)
            return

        # User Profile & Friends
        if path in ('/api/user-profile', '/api/auth/profile'):
            res, code = auth_controller.handle_get_profile(params)
            self.send_json_response(res, code)
            return

        if path == '/api/auth/friends':
            res, code = auth_controller.handle_get_friends(params)
            self.send_json_response(res, code)
            return

        # Chat
        if path == '/api/chat/messages':
            res, code = chat_controller.handle_get_group_messages(params)
            self.send_json_response(res, code)
            return

        if path == '/api/chat/direct':
            res, code = chat_controller.handle_get_direct_messages(params)
            self.send_json_response(res, code)
            return

        # Authentication Session
        if path == '/api/auth/session':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip() if 'Bearer ' in auth_header else params.get('token', [None])[0]
            res, code = auth_controller.handle_validate_session(token)
            self.send_json_response(res, code)
            return

        # Vault Documents
        if path == '/api/vault/list':
            res, code = vault_controller.handle_list_vault(params)
            self.send_json_response(res, code)
            return

        # Notifications & Activity
        if path == '/api/notifications':
            res, code = admin_controller.handle_get_notifications(params)
            self.send_json_response(res, code)
            return

        if path == '/api/activity':
            res, code = admin_controller.handle_get_activity(params)
            self.send_json_response(res, code)
            return

        # Universal Global Search
        if path == '/api/search':
            auth_header = self.headers.get('Authorization', '')
            token = auth_header.replace('Bearer ', '').strip() if 'Bearer ' in auth_header else params.get('token', [None])[0]
            res, code = admin_controller.handle_global_search(params, token)
            self.send_json_response(res, code)
            return

        # Admin Telemetry & Audit Logs
        if path == '/api/admin/metrics':
            res, code = admin_controller.handle_admin_metrics()
            self.send_json_response(res, code)
            return

        if path == '/api/admin/audit-logs':
            res, code = admin_controller.handle_get_audit_logs(params)
            self.send_json_response(res, code)
            return

        if path == '/api/users' or path == '/api/admin/users':
            res, code = admin_controller.handle_admin_list_users(params)
            self.send_json_response(res, code)
            return

        # Fallback to SPA root for frontend routes if file doesn't exist
        file_path = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
        if not os.path.exists(file_path) and not path.startswith('/api'):
            self.path = '/index.html'

        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        try:
            body = json.loads(post_data)
        except Exception:
            body = {}

        # AI Endpoints
        if path == '/api/ai/chat':
            res, code = ai_controller.handle_ai_chat(body)
            self.send_json_response(res, code)
            return

        if path == '/api/ai/scan-receipt':
            res, code = ai_controller.handle_ai_scan_receipt(body)
            self.send_json_response(res, code)
            return

        if path == '/api/ai/insights':
            res, code = ai_controller.handle_ai_insights(body)
            self.send_json_response(res, code)
            return

        # Groups
        if path in ('/api/save-group', '/api/groups/save'):
            res, code = group_controller.handle_save_group(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/join':
            res, code = group_controller.handle_join_group(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/members/add':
            res, code = group_controller.handle_add_member(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/members/remove':
            res, code = group_controller.handle_remove_member(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/members/role':
            res, code = group_controller.handle_update_member_role(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/settings/update':
            res, code = group_controller.handle_update_group_settings(body)
            self.send_json_response(res, code)
            return

        if path == '/api/groups/delete':
            res, code = group_controller.handle_delete_group(body)
            self.send_json_response(res, code)
            return

        # Expenses & Settlements
        if path == '/api/expenses/add':
            res, code = expense_controller.handle_add_expense(body)
            self.send_json_response(res, code)
            return

        if path == '/api/expenses/delete':
            res, code = expense_controller.handle_delete_expense(body)
            self.send_json_response(res, code)
            return

        if path in ('/api/expenses/claim', '/api/expenses/claim-settlement'):
            res, code = expense_controller.handle_claim_payment(body)
            self.send_json_response(res, code)
            return

        if path == '/api/expenses/confirm-claim':
            res, code = expense_controller.handle_confirm_claim(body)
            self.send_json_response(res, code)
            return

        if path == '/api/expenses/decline-claim':
            res, code = expense_controller.handle_decline_claim(body)
            self.send_json_response(res, code)
            return

        if path == '/api/expenses/settle-direct':
            res, code = expense_controller.handle_direct_settlement(body)
            self.send_json_response(res, code)
            return

        # Chat
        if path == '/api/chat/send':
            res, code = chat_controller.handle_send_group_message(body)
            self.send_json_response(res, code)
            return

        if path == '/api/chat/react':
            res, code = chat_controller.handle_react_message(body)
            self.send_json_response(res, code)
            return

        if path == '/api/chat/direct/send':
            res, code = chat_controller.handle_send_direct_message(body)
            self.send_json_response(res, code)
            return

        # Authentication & Accounts
        if path == '/api/auth/register':
            res, code = auth_controller.handle_register(body)
            self.send_json_response(res, code)
            return

        if path == '/api/auth/login':
            res, code = auth_controller.handle_login(body)
            self.send_json_response(res, code)
            return

        if path == '/api/auth/logout':
            res, code = auth_controller.handle_logout(body)
            self.send_json_response(res, code)
            return

        # User Profile, Friends, Account
        if path in ('/api/save-profile', '/api/auth/profile'):
            res, code = auth_controller.handle_save_profile(body)
            self.send_json_response(res, code)
            return

        if path == '/api/auth/friends/add':
            res, code = auth_controller.handle_add_friend(body)
            self.send_json_response(res, code)
            return

        if path == '/api/admin/users/role':
            res, code = admin_controller.handle_admin_set_user_role(body)
            self.send_json_response(res, code)
            return

        if path == '/api/admin/users/delete':
            res, code = admin_controller.handle_admin_delete_user(body)
            self.send_json_response(res, code)
            return

        if path == '/api/auth/delete-account':
            res, code = auth_controller.handle_delete_account(body)
            self.send_json_response(res, code)
            return

        # Vault
        if path == '/api/vault/upload':
            res, code = vault_controller.handle_upload_vault(body)
            self.send_json_response(res, code)
            return

        if path == '/api/vault/delete':
            res, code = vault_controller.handle_delete_vault(body)
            self.send_json_response(res, code)
            return

        # Notifications
        if path == '/api/notifications/read':
            res, code = admin_controller.handle_mark_notification_read(body)
            self.send_json_response(res, code)
            return

        self.send_response(404)
        self.end_headers()

    def send_json_response(self, data, status_code=200):
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-User-Id')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(response_bytes)
        try:
            self.wfile.flush()
        except Exception:
            pass

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-User-Id')
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    init_db()
    ensure_seed_users()
    from backend.repositories.group_repo import ensure_seed_groups
    ensure_seed_groups()
    print("============================================================")
    print("  SplitEase Pro FinTech 3.0 -- Layered Architecture Server")
    print(f"  Serving React Platform at: http://localhost:{PORT}")
    print(f"  AI Engine: Google Gemini ({GEMINI_MODEL})")
    print("  Firebase Project: splitease-9b53d")
    print("  Database: SQLite Layered + Dual Cloud")
    print("============================================================")
    
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), SplitEaseRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped gracefully.")
