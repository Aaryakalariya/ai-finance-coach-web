"""
security.py - CSRF tokens, OTP generation, and misc security helpers.
"""

import secrets
import string
import hashlib
from datetime import datetime, timedelta

from utils.constants import OTP_LENGTH, OTP_EXPIRY_MINUTES


def generate_csrf_token() -> str:
    """Generate a random CSRF token to store in the session."""
    return secrets.token_hex(32)


def generate_otp(length: int = OTP_LENGTH) -> str:
    """Generate a numeric one-time password."""
    return "".join(secrets.choice(string.digits) for _ in range(length))


def otp_expiry_time(minutes: int = OTP_EXPIRY_MINUTES) -> datetime:
    """Return the timestamp at which a freshly-generated OTP should expire."""
    return datetime.utcnow() + timedelta(minutes=minutes)


def generate_secure_token(nbytes: int = 32) -> str:
    """Generate a URL-safe secure random token (e.g. for password-reset links)."""
    return secrets.token_urlsafe(nbytes)


def hash_token(token: str) -> str:
    """Hash a token before storing it in the database (never store raw tokens)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def constant_time_compare(a: str, b: str) -> bool:
    """Timing-safe string comparison, useful for comparing tokens/OTPs."""
    return secrets.compare_digest(a, b)


def sanitize_filename(filename: str) -> str:
    """Strip potentially dangerous characters from an uploaded filename."""
    keep_chars = "-_.() "
    return "".join(c for c in filename if c.isalnum() or c in keep_chars).strip()