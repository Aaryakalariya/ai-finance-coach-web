"""
constants.py - Shared constants used across the AI Finance Coach application.
"""

# Payment methods available when logging an expense
PAYMENT_METHODS = ["Cash", "Card", "UPI", "Bank Transfer", "Wallet", "Other"]

# Report types and export formats
REPORT_TYPES = ["monthly", "category", "yearly"]
REPORT_FORMATS = ["pdf", "excel", "csv"]

# Supported currencies
CURRENCIES = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

DEFAULT_CURRENCY = "INR"

# Account / user status values
USER_STATUS_ACTIVE = "active"
USER_STATUS_SUSPENDED = "suspended"

# Notification categories (used for icon selection)
NOTIFICATION_ICONS = {
    "budget_alert": "bi-exclamation-triangle",
    "goal_reached": "bi-trophy",
    "new_feature": "bi-stars",
    "system": "bi-info-circle",
    "reminder": "bi-bell",
}

# OTP configuration
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 10
OTP_MAX_ATTEMPTS = 5

# Session / auth configuration
SESSION_LIFETIME_DAYS = 7
PASSWORD_MIN_LENGTH = 8

# AI configuration
AI_DEFAULT_DAILY_LIMIT = 20
AI_MAX_MESSAGE_LENGTH = 2000

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Budget alert thresholds (percentage of limit used)
BUDGET_WARNING_THRESHOLD = 70
BUDGET_DANGER_THRESHOLD = 90

# File upload limits
MAX_AVATAR_SIZE_MB = 5
ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}