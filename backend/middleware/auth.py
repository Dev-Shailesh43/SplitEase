"""
Auth Middleware — Token & session extraction.
"""

def extract_user(headers):
    auth_header = headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:].strip()
        # If demo token or custom uid passed
        if token.startswith('usr_') or token.startswith('demo_'):
            return {"uid": token, "authenticated": True}
        # In full production mode, Firebase ID tokens can be decoded
        return {"uid": token, "authenticated": True}
    
    # Fallback to custom User-Id header if provided
    uid = headers.get('X-User-Id')
    if uid:
        return {"uid": uid, "authenticated": True}
    return None
