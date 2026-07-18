"""
use_model.py - User data access (registration, login, profile, preferences).
Note: filename matches the project's existing naming (use_model.py for "user model").
"""

from database.db_connection import fetch_one, fetch_all, execute
from utils.password_hash import hash_password


class UserModel:

    @staticmethod
    def create(full_name: str, email: str, password: str, phone: str = None) -> int:
        """Create a new user and return their new id."""
        password_hash = hash_password(password)
        query = """
            INSERT INTO users (full_name, email, password_hash, phone)
            VALUES (%s, %s, %s, %s)
        """
        return execute(query, (full_name, email, password_hash, phone))

    @staticmethod
    def get_by_id(user_id: int) -> dict:
        return fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))

    @staticmethod
    def get_by_email(email: str) -> dict:
        return fetch_one("SELECT * FROM users WHERE email = %s", (email,))

    @staticmethod
    def email_exists(email: str) -> bool:
        return UserModel.get_by_email(email) is not None

    @staticmethod
    def update_profile(user_id: int, full_name: str, phone: str, currency: str) -> None:
        query = """
            UPDATE users SET full_name = %s, phone = %s, currency = %s
            WHERE id = %s
        """
        execute(query, (full_name, phone, currency, user_id))

    @staticmethod
    def update_avatar(user_id: int, avatar_url: str) -> None:
        execute("UPDATE users SET avatar_url = %s WHERE id = %s", (avatar_url, user_id))

    @staticmethod
    def update_password(user_id: int, new_password: str) -> None:
        password_hash = hash_password(new_password)
        execute("UPDATE users SET password_hash = %s WHERE id = %s", (password_hash, user_id))

    @staticmethod
    def mark_email_verified(user_id: int) -> None:
        execute("UPDATE users SET email_verified = TRUE WHERE id = %s", (user_id,))

    @staticmethod
    def set_status(user_id: int, status: str) -> None:
        execute("UPDATE users SET status = %s WHERE id = %s", (status, user_id))

    @staticmethod
    def delete(user_id: int) -> None:
        execute("DELETE FROM users WHERE id = %s", (user_id,))

    @staticmethod
    def get_all(search: str = None, limit: int = 50, offset: int = 0) -> list:
        if search:
            query = """
                SELECT * FROM users
                WHERE full_name LIKE %s OR email LIKE %s
                ORDER BY created_at DESC LIMIT %s OFFSET %s
            """
            like = f"%{search}%"
            return fetch_all(query, (like, like, limit, offset))
        query = "SELECT * FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s"
        return fetch_all(query, (limit, offset))

    @staticmethod
    def count_total() -> int:
        row = fetch_one("SELECT COUNT(*) AS total FROM users")
        return row["total"] if row else 0

    @staticmethod
    def count_active_today() -> int:
        row = fetch_one(
            """
            SELECT COUNT(DISTINCT user_id) AS total FROM activity_logs
            WHERE DATE(created_at) = CURDATE()
            """
        )
        return row["total"] if row else 0

    # --- Preferences ---

    @staticmethod
    def get_preferences(user_id: int) -> dict:
        return fetch_one("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))

    @staticmethod
    def update_preferences(user_id: int, email_notifications: bool, budget_alerts: bool, dark_mode: bool) -> None:
        query = """
            UPDATE user_preferences
            SET email_notifications = %s, budget_alerts = %s, dark_mode = %s
            WHERE user_id = %s
        """
        execute(query, (email_notifications, budget_alerts, dark_mode, user_id))