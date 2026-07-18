"""
saving_model.py - Savings goals & contributions data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class SavingsModel:

    @staticmethod
    def create(user_id: int, name: str, target_amount: float, target_date: str) -> int:
        query = """
            INSERT INTO savings_goals (user_id, name, target_amount, target_date)
            VALUES (%s, %s, %s, %s)
        """
        return execute(query, (user_id, name, target_amount, target_date))

    @staticmethod
    def get_by_id(goal_id: int) -> dict:
        return fetch_one("SELECT * FROM savings_goals WHERE id = %s", (goal_id,))

    @staticmethod
    def get_for_user(user_id: int) -> list:
        return fetch_all(
            "SELECT * FROM savings_goals WHERE user_id = %s ORDER BY target_date ASC", (user_id,)
        )

    @staticmethod
    def update(goal_id: int, name: str, target_amount: float, target_date: str) -> None:
        query = """
            UPDATE savings_goals SET name = %s, target_amount = %s, target_date = %s
            WHERE id = %s
        """
        execute(query, (name, target_amount, target_date, goal_id))

    @staticmethod
    def delete(goal_id: int) -> None:
        execute("DELETE FROM savings_goals WHERE id = %s", (goal_id,))

    @staticmethod
    def add_contribution(goal_id: int, amount: float) -> int:
        """Insert a contribution; a DB trigger updates savings_goals.current_amount automatically."""
        return execute(
            "INSERT INTO savings_contributions (goal_id, amount) VALUES (%s, %s)",
            (goal_id, amount),
        )

    @staticmethod
    def get_total_saved(user_id: int) -> float:
        query = "SELECT COALESCE(SUM(current_amount), 0) AS total FROM savings_goals WHERE user_id = %s"
        row = fetch_one(query, (user_id,))
        return float(row["total"]) if row else 0.0

    @staticmethod
    def count_goals(user_id: int) -> int:
        row = fetch_one("SELECT COUNT(*) AS total FROM savings_goals WHERE user_id = %s", (user_id,))
        return row["total"] if row else 0