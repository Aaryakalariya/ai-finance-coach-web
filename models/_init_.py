"""
models package - data access layer for AI Finance Coach.

Each *_model.py module exposes plain functions (not ORM classes) that wrap
raw SQL queries via database.db_connection. Controllers/services import
from here rather than writing SQL directly.
"""

from models.use_model import UserModel
from models.admin_model import AdminModel
from models.category_model import CategoryModel
from models.expense_model import ExpenseModel
from models.income_model import IncomeModel
from models.budget_model import BudgetModel
from models.saving_model import SavingsModel
from models.notification_model import NotificationModel
from models.ai_log_model import AiLogModel
from models.report_model import ReportModel

__all__ = [
    "UserModel",
    "AdminModel",
    "CategoryModel",
    "ExpenseModel",
    "IncomeModel",
    "BudgetModel",
    "SavingsModel",
    "NotificationModel",
    "AiLogModel",
    "ReportModel",
]