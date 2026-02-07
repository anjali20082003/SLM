"""Development settings."""
import os
from pathlib import Path

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Use SQLite for easy local dev if no DB_* set
if not os.environ.get("DB_NAME"):
    _base = Path(__file__).resolve().parent.parent.parent
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(_base / "db.sqlite3"),
        }
    }

CORS_ALLOW_ALL_ORIGINS = True
