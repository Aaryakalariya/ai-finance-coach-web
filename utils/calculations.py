"""
calculations.py - Core financial calculation helpers (totals, budgets, predictions).
"""

from datetime import date
from decimal import Decimal, ROUND_HALF_UP


def to_decimal(value) -> Decimal:
    """Safely coerce a value to Decimal for money math."""
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal("0")


def sum_amounts(records, key: str = "amount") -> Decimal:
    """Sum a list of dict-like records by a given key."""
    total = Decimal("0")
    for record in records or []:
        total += to_decimal(record.get(key, 0))
    return total


def calculate_budget_usage(spent, limit) -> float:
    """Return percentage of a budget used, capped for display purposes at the caller's discretion."""
    spent = to_decimal(spent)
    limit = to_decimal(limit)
    if limit == 0:
        return 0.0
    pct = (spent / limit) * Decimal("100")
    return float(pct.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def calculate_savings_progress(current, target) -> float:
    """Return percentage progress toward a savings goal."""
    return calculate_budget_usage(current, target)


def net_balance(total_income, total_expenses) -> Decimal:
    """Simple income minus expenses calculation."""
    return to_decimal(total_income) - to_decimal(total_expenses)


def predict_next_month_spend(monthly_totals: list) -> float:
    """
    Naive prediction of next month's spend based on a simple moving average
    of the last up-to-3 months of totals. Replace with a real model / the
    prediction_service for anything more sophisticated.
    """
    if not monthly_totals:
        return 0.0
    recent = monthly_totals[-3:]
    avg = sum(to_decimal(v) for v in recent) / Decimal(len(recent))
    return float(avg.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def days_until(target_date) -> int:
    """Number of calendar days remaining until a target date (can be negative if past)."""
    if isinstance(target_date, str):
        from datetime import datetime
        target_date = datetime.fromisoformat(target_date).date()
    return (target_date - date.today()).days


def required_monthly_contribution(target_amount, current_amount, target_date) -> float:
    """How much a user needs to save per month to hit a savings goal on time."""
    remaining = to_decimal(target_amount) - to_decimal(current_amount)
    if remaining <= 0:
        return 0.0
    days_left = max(days_until(target_date), 1)
    months_left = max(days_left / 30.0, 1)
    return float((remaining / Decimal(str(months_left))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))