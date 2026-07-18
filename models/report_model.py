"""
report_model.py - Generated report metadata data access.
"""

from database.db_connection import fetch_one, fetch_all, execute


class ReportModel:

    @staticmethod
    def create(user_id, name: str, report_type: str, report_format: str, file_path: str) -> int:
        query = """
            INSERT INTO reports (user_id, name, type, format, file_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        return execute(query, (user_id, name, report_type, report_format, file_path))

    @staticmethod
    def get_by_id(report_id: int) -> dict:
        return fetch_one("SELECT * FROM reports WHERE id = %s", (report_id,))

    @staticmethod
    def get_for_user(user_id: int) -> list:
        query = """
            SELECT * FROM reports WHERE user_id = %s
            ORDER BY generated_at DESC
        """
        return fetch_all(query, (user_id,))

    @staticmethod
    def get_all_for_admin() -> list:
        query = """
            SELECT r.*, u.full_name AS user_name FROM reports r
            LEFT JOIN users u ON u.id = r.user_id
            WHERE r.user_id IS NULL
            ORDER BY r.generated_at DESC
        """
        return fetch_all(query)

    @staticmethod
    def delete(report_id: int) -> None:
        execute("DELETE FROM reports WHERE id = %s", (report_id,))