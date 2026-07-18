"""
helper.py - Miscellaneous small helpers used across controllers/services.
"""

import os
import uuid
from datetime import datetime

from utils.constants import ALLOWED_AVATAR_EXTENSIONS, MAX_AVATAR_SIZE_MB
from utils.security import sanitize_filename


def current_month_year() -> str:
    """Return the current month in 'YYYY-MM' format, used for budget lookups."""
    return datetime.utcnow().strftime("%Y-%m")


def generate_unique_filename(original_filename: str) -> str:
    """Generate a collision-safe filename while preserving the extension."""
    safe_name = sanitize_filename(original_filename)
    ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
    return f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex


def is_allowed_avatar(filename: str, file_size_bytes: int) -> tuple[bool, str]:
    """Validate an uploaded avatar image's extension and size."""
    if "." not in filename:
        return False, "File must have an extension."
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        return False, f"Unsupported file type: .{ext}"
    max_bytes = MAX_AVATAR_SIZE_MB * 1024 * 1024
    if file_size_bytes > max_bytes:
        return False, f"File too large. Max size is {MAX_AVATAR_SIZE_MB}MB."
    return True, ""


def paginate(query_results: list, page: int = 1, page_size: int = 20) -> dict:
    """Simple in-memory pagination helper for small result sets."""
    page = max(page, 1)
    total = len(query_results)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": query_results[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": max((total + page_size - 1) // page_size, 1),
    }


def safe_get(dictionary: dict, *keys, default=None):
    """Safely walk a nested dict: safe_get(data, 'user', 'profile', 'name')."""
    current = dictionary
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def build_upload_path(base_dir: str, subfolder: str, filename: str) -> str:
    """Build and ensure an upload directory exists, returning the full file path."""
    directory = os.path.join(base_dir, subfolder)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, filename)