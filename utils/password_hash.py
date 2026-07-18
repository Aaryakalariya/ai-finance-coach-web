"""
password_hash.py - Password hashing helpers using Werkzeug's PBKDF2 implementation.
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage."""
    return generate_password_hash(plain_password, method="pbkdf2:sha256", salt_length=16)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Check a plaintext password against a stored hash."""
    if not password_hash:
        return False
    return check_password_hash(password_hash, plain_password)


def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Basic password strength check.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""