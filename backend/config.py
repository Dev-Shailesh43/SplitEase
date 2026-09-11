"""
SplitEase Pro — Backend Configuration
Centralized configuration settings, API keys, database paths, and constants.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "splitease_v2.db")
PORT = 5000

# Google Gemini API Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-flash-latest"

# Local .env loader (ignored by Git for secret protection)
_env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(_env_path):
    try:
        with open(_env_path, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line.startswith("GEMINI_API_KEY="):
                    GEMINI_API_KEY = _line.split("=", 1)[1].strip(' "\'')
    except Exception:
        pass

# Firebase Cloud Firestore & Storage Config
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyAMUU_Od3W3Xgl7JW6X58oM76zucYsH0RY",
    "authDomain": "splitease-9b53d.firebaseapp.com",
    "projectId": "splitease-9b53d",
    "storageBucket": "splitease-9b53d.firebasestorage.app",
    "messagingSenderId": "757354576492",
    "appId": "1:757354576492:web:fab8f8045f398f10867649"
}
