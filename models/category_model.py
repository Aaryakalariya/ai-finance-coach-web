"""
category_model.py - Expense/income category data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class CategoryModel:

    @staticmethod
    def get_all(category_type: str = None) -> list:
        if category_type:
            return fetch_all(
                "SELECT * FROM categories WHERE type = %s ORDER BY name", (category_type,)
            )
        return fetch_all("SELECT * FROM categories ORDER BY type, name")

    @staticmethod
    def get_by_id(category_id: int) -> dict:
        return fetch_one("SELECT * FROM categories WHERE id = %s", (category_id,))

    @staticmethod
    def create(name: str, icon: str, category_type: str) -> int:
        query = "INSERT INTO categories (name, icon, type) VALUES (%s, %s, %s)"
        return execute(query, (name, icon, category_type))

    @staticmethod
    def update(category_id: int, name: str, icon: str) -> None:
        execute("UPDATE categories SET name = %s, icon = %s WHERE id = %s", (name, icon, category_id))

    @staticmethod
    def delete(category_id: int) -> None:
        execute("DELETE FROM categories WHERE id = %s", (category_id,))

    @staticmethod
    def get_with_usage_counts() -> list:
        query = """
            SELECT c.*,
                (SELECT COUNT(*) FROM expenses e WHERE e.category_id = c.id) AS usage_count
            FROM categories c
            ORDER BY c.type, c.name
        """
        return fetch_all(query)

    @staticmethod
    def get_most_used(limit: int = 5) -> list:
        query = """
            SELECT c.name, COUNT(e.id) AS usage_count
            FROM categories c
            JOIN expenses e ON e.category_id = c.id
            GROUP BY c.id
            ORDER BY usage_count DESC
            LIMIT %s
        """
        return fetch_all(query, (limit,))