"""
Error Handler — Standardized JSON responses for error handling.
"""

def make_error_response(message, code=400, details=None):
    res = {
        "status": "error",
        "code": code,
        "message": message
    }
    if details:
        res["details"] = details
    return res, code

def make_success_response(data=None, message="Success", code=200):
    res = {
        "status": "success",
        "message": message
    }
    if data is not None:
        res.update(data)
    return res, code
