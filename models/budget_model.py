"""
budget_model.py - Budget data access.
"""

from database.db_connection import fetch_one, fetch_all, execute, call_procedure


class BudgetModel:

    @staticmethod
    def create(user_id: int, category_id: int, monthly_limit: float, month_year: str) -> int:
        query = """
            INSERT INTO budgets (user_id, category_id, monthly_limit, month_year)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE monthly_limit = VALUES(monthly_limit)
        """
        return execute(query, (user_id, category_id, monthly_limit, month_year))

    @staticmethod
    def get_by_id(budget_id: int) -> dict:
        return fetch_one("SELECT * FROM budgets WHERE id = %s", (budget_id,))

    @staticmethod
    def get_for_user_month(user_id: int, month_year: str) -> list:
        """Budgets with amount spent, computed via the sp_get_budget_utilization procedure."""
        try:
            results = call_procedure("sp_get_budget_utilization", (user_id, month_year))
            return results[0] if results else []
        except Exception:
            # Fallback to a plain query if the stored procedure isn't installed
            query = """
                SELECT b.id, c.name AS category_name, b.monthly_limit AS `limit`,
                    COALESCE((
                        SELECT SUM(e.amount) FROM expenses e
                        WHERE e.user_id = b.user_id AND e.category_id = b.category_id
                        AND DATE_FORMAT(e.date, '%%Y-%%m') = b.month_year
                    ), 0) AS spent
                FROM budgets b
                JOIN categories c ON c.id = b.category_id
                WHERE b.user_id = %s AND b.month_year = %s
            """
            return fetch_all(query, (user_id, month_year))

    @staticmethod
    def update(budget_id: int, monthly_limit: float) -> None:
        execute("UPDATE budgets SET monthly_limit = %s WHERE id = %s", (monthly_limit, budget_id))

    @staticmethod
    def delete(budget_id: int) -> None:
        execute("DELETE FROM budgets WHERE id = %s", (budget_id,))

    @staticmethod
    def get_overall_usage_percent(user_id: int, month_year: str) -> float:
        budgets = BudgetModel.get_for_user_month(user_id, month_year)
        total_limit = sum(float(b.get("monthly_limit") or b.get("limit") or 0) for b in budgets)
        total_spent = sum(float(b.get("spent") or 0) for b in budgets)
        if total_limit == 0:
            return 0.0
        return round((total_spent / total_limit) * 100, 1)