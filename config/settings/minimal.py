"""Minimal settings: no Celery, Channels, or OTP. Use with requirements-minimal.txt."""
import os
from pathlib import Path
from .base import *  # noqa: F401, F403

# Use SQLite when no DB is configured
if not os.environ.get("DB_NAME"):
    _base = Path(__file__).resolve().parent.parent.parent
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(_base / "db.sqlite3"),
        }
    }

# Remove apps that require extra deps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "slm",
]

# Remove OTP and audit middleware that may depend on otp
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "slm.middleware.AuditLogMiddleware",
    "slm.middleware.RoleBasedAccessMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
