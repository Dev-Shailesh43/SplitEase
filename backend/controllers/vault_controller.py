"""
Vault Controller — Document uploads, bills, invoices, and categorization.
"""

from ..repositories.vault_repo import save_vault_file, list_vault_files, delete_vault_file, get_vault_file
from ..repositories.notification_repo import log_audit, log_activity
from ..middleware.error_handler import make_success_response, make_error_response

def handle_list_vault(params):
    group_id = params.get('groupId', [None])[0]
    files = list_vault_files(group_id)
    return make_success_response({"files": files})

def handle_upload_vault(body):
    group_id = body.get('groupId', 'general')
    filename = body.get('filename', 'document.pdf')
    category = body.get('category', 'Receipt')
    uploaded_by = body.get('uploadedBy', 'Member')
    file_data = body.get('fileData', '')

    if not file_data:
        return make_error_response("Missing fileData payload", 400)

    saved_file = save_vault_file(group_id, filename, category, uploaded_by, file_data)
    log_activity(
        group_id=group_id,
        user_id='usr',
        user_name=uploaded_by,
        action="uploaded_file",
        details=f"Uploaded '{filename}' to {category}"
    )

    return make_success_response({"file": saved_file, "message": "File stored in vault successfully"})

def handle_delete_vault(body):
    file_id = body.get('fileId')
    if not file_id:
        return make_error_response("Missing fileId", 400)
    delete_vault_file(file_id)
    return make_success_response({"message": "File deleted from vault"})
