"""Encryption for sensitive model fields."""
import base64
import hashlib
from django.conf import settings
from cryptography.fernet import Fernet


def get_fernet():
    """Derive a valid Fernet key (32 bytes, base64) from settings."""
    raw = (settings.FIELD_ENCRYPTION_KEY or "default-key")[:32].ljust(32, "0")
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    digest = hashlib.sha256(raw).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def encrypt_value(value: str) -> str:
    if not value:
        return value
    try:
        return get_fernet().encrypt(value.encode()).decode()
    except Exception:
        return value


def decrypt_value(value: str) -> str:
    if not value:
        return value
    try:
        return get_fernet().decrypt(value.encode()).decode()
    except Exception:
        return value
