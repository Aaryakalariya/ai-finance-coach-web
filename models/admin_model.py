"""
admin_model.py - Admin account data access and platform settings.
"""

from database.db_connection import fetch_one, fetch_all, execute
from utils.password_hash import hash_password


class AdminModel:

    @staticmethod
    def get_by_email(email: str) -> dict:
        return fetch_one("SELECT * FROM admins WHERE email = %s", (email,))

    @staticmethod
    def get_by_id(admin_id: int) -> dict:
        return fetch_one("SELECT * FROM admins WHERE id = %s", (admin_id,))

    @staticmethod
    def create(full_name: str, email: str, password: str, role: str = "support") -> int:
        password_hash = hash_password(password)
        query = """
            INSERT INTO admins (full_name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """
        return execute(query, (full_name, email, password_hash, role))

    # --- Platform settings (singleton row, id = 1) ---

    @staticmethod
    def get_settings() -> dict:
        return fetch_one("SELECT * FROM platform_settings WHERE id = 1")

    @staticmethod
    def update_settings(platform_name: str, support_email: str, maintenance_mode: bool, allow_registrations: bool) -> None:
        query = """
            UPDATE platform_settings
            SET platform_name = %s, support_email = %s,
                maintenance_mode = %s, allow_registrations = %s
            WHERE id = 1
        """
        execute(query, (platform_name, support_email, maintenance_mode, allow_registrations))

    @staticmethod
    def update_ai_settings(ai_daily_limit: int, ai_model: str) -> None:
        query = "UPDATE platform_settings SET ai_daily_limit = %s, ai_model = %s WHERE id = 1"
        execute(query, (ai_daily_limit, ai_model))

    # --- Activity logs ---

    @staticmethod
    def log_activity(user_id: int, action: str, ip_address: str = None) -> None:
        query = "INSERT INTO activity_logs (user_id, action, ip_address) VALUES (%s, %s, %s)"
        execute(query, (user_id, action, ip_address))

    @staticmethod
    def get_activity_logs(limit: int = 100) -> list:
        query = """
            SELECT al.*, u.full_name AS user_name
            FROM activity_logs al
            LEFT JOIN users u ON u.id = al.user_id
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return fetch_all(query, (limit,))

    @staticmethod
    def get_recent_activity(limit: int = 10) -> list:
        query = """
            SELECT u.full_name AS user, al.action, al.created_at AS timestamp
            FROM activity_logs al
            LEFT JOIN users u ON u.id = al.user_id
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return fetch_all(query, (limit,))

    # --- Feedback ---

    @staticmethod
    def get_all_feedback() -> list:
        query = """
            SELECT f.*, u.full_name AS user_name
            FROM feedback f
            JOIN users u ON u.id = f.user_id
            ORDER BY f.created_at DESC
        """
        return fetch_all(query)