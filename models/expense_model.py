"""
expense_model.py - Expense data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class ExpenseModel:

    @staticmethod
    def create(user_id: int, category_id: int, description: str, amount: float,
                payment_method: str, expense_date: str) -> int:
        query = """
            INSERT INTO expenses (user_id, category_id, description, amount, payment_method, date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute(query, (user_id, category_id, description, amount, payment_method, expense_date))

    @staticmethod
    def get_by_id(expense_id: int) -> dict:
        return fetch_one("SELECT * FROM expenses WHERE id = %s", (expense_id,))

    @staticmethod
    def get_for_user(user_id: int, category_id: int = None, from_date: str = None, to_date: str = None) -> list:
        query = """
            SELECT e.*, c.name AS category_name
            FROM expenses e
            LEFT JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = %s
        """
        params = [user_id]
        if category_id:
            query += " AND e.category_id = %s"
            params.append(category_id)
        if from_date:
            query += " AND e.date >= %s"
            params.append(from_date)
        if to_date:
            query += " AND e.date <= %s"
            params.append(to_date)
        query += " ORDER BY e.date DESC"
        return fetch_all(query, tuple(params))

    @staticmethod
    def get_recent(user_id: int, limit: int = 5) -> list:
        query = """
            SELECT e.*, c.name AS category_name
            FROM expenses e
            LEFT JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = %s
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT %s
        """
        return fetch_all(query, (user_id, limit))

    @staticmethod
    def update(expense_id: int, description: str, amount: float, category_id: int,
                payment_method: str, expense_date: str) -> None:
        query = """
            UPDATE expenses
            SET description = %s, amount = %s, category_id = %s, payment_method = %s, date = %s
            WHERE id = %s
        """
        execute(query, (description, amount, category_id, payment_method, expense_date, expense_id))

    @staticmethod
    def delete(expense_id: int) -> None:
        execute("DELETE FROM expenses WHERE id = %s", (expense_id,))

    @staticmethod
    def get_total_for_month(user_id: int, month_year: str) -> float:
        query = """
            SELECT COALESCE(SUM(amount), 0) AS total FROM expenses
            WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s
        """
        row = fetch_one(query, (user_id, month_year))
        return float(row["total"]) if row else 0.0

    @staticmethod
    def get_category_breakdown(user_id: int, month_year: str) -> list:
        query = """
            SELECT c.name AS category, SUM(e.amount) AS total
            FROM expenses e
            JOIN categories c ON c.id = e.category_id
            WHERE e.user_id = %s AND DATE_FORMAT(e.date, '%%Y-%%m') = %s
            GROUP BY c.id
            ORDER BY total DESC
        """
        return fetch_all(query, (user_id, month_year))

    @staticmethod
    def get_monthly_totals(user_id: int, months: int = 6) -> list:
        query = """
            SELECT DATE_FORMAT(date, '%%Y-%%m') AS month, SUM(amount) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY month
            ORDER BY month DESC
            LIMIT %s
        """
        return fetch_all(query, (user_id, months))

    @staticmethod
    def get_all_for_admin(expense_type: str = None, from_date: str = None, to_date: str = None) -> list:
        query = """
            SELECT e.*, u.full_name AS user_name, 'expense' AS type
            FROM expenses e
            JOIN users u ON u.id = e.user_id
            WHERE 1=1
        """
        params = []
        if from_date:
            query += " AND e.date >= %s"
            params.append(from_date)
        if to_date:
            query += " AND e.date <= %s"
            params.append(to_date)
        query += " ORDER BY e.date DESC"
        return fetch_all(query, tuple(params))