"""
income_model.py - Income data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class IncomeModel:

    @staticmethod
    def create(user_id: int, source: str, description: str, amount: float, income_date: str) -> int:
        query = """
            INSERT INTO income (user_id, source, description, amount, date)
            VALUES (%s, %s, %s, %s, %s)
        """
        return execute(query, (user_id, source, description, amount, income_date))

    @staticmethod
    def get_by_id(income_id: int) -> dict:
        return fetch_one("SELECT * FROM income WHERE id = %s", (income_id,))

    @staticmethod
    def get_for_user(user_id: int) -> list:
        return fetch_all("SELECT * FROM income WHERE user_id = %s ORDER BY date DESC", (user_id,))

    @staticmethod
    def update(income_id: int, source: str, description: str, amount: float, income_date: str) -> None:
        query = """
            UPDATE income SET source = %s, description = %s, amount = %s, date = %s
            WHERE id = %s
        """
        execute(query, (source, description, amount, income_date, income_id))

    @staticmethod
    def delete(income_id: int) -> None:
        execute("DELETE FROM income WHERE id = %s", (income_id,))

    @staticmethod
    def get_total_for_month(user_id: int, month_year: str) -> float:
        query = """
            SELECT COALESCE(SUM(amount), 0) AS total FROM income
            WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s
        """
        row = fetch_one(query, (user_id, month_year))
        return float(row["total"]) if row else 0.0

    @staticmethod
    def get_monthly_totals(user_id: int, months: int = 6) -> list:
        query = """
            SELECT DATE_FORMAT(date, '%%Y-%%m') AS month, SUM(amount) AS total
            FROM income
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month DESC
            LIMIT %s
        """
        return fetch_all(query, (user_id, months))