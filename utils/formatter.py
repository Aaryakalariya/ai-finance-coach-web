"""
formatter.py - Currency, date, and display formatting helpers.
"""

from datetime import datetime, date
from utils.constants import CURRENCIES, DEFAULT_CURRENCY


def format_currency(amount, currency: str = DEFAULT_CURRENCY) -> str:
    """Format a numeric amount as a currency string, e.g. 1500.5 -> '₹1,500.50'."""
    symbol = CURRENCIES.get(currency, DEFAULT_CURRENCY)
    try:
        return f"{symbol}{float(amount):,.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0.00"


def format_date(value, fmt: str = "%b %d, %Y") -> str:
    """Format a date/datetime/ISO string into a readable string."""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    if isinstance(value, (datetime, date)):
        return value.strftime(fmt)
    return str(value)


def format_percent(value, decimals: int = 0) -> str:
    """Format a numeric ratio/percentage for display, e.g. 72.345 -> '72%'."""
    try:
        return f"{float(value):.{decimals}f}%"
    except (TypeError, ValueError):
        return "0%"


def truncate(text: str, length: int = 100, suffix: str = "...") -> str:
    """Truncate long text (e.g. AI prompts/responses) for table display."""
    if not text:
        return ""
    if len(text) <= length:
        return text
    return text[: length - len(suffix)].rstrip() + suffix


def month_year_label(month_year: str) -> str:
    """Convert '2026-07' into 'July 2026'."""
    try:
        dt = datetime.strptime(month_year, "%Y-%m")
        return dt.strftime("%B %Y")
    except (ValueError, TypeError):
        return month_year