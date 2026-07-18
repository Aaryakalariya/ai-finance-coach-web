"""
db_connection.py - MySQL connection pool and query helpers for AI Finance Coach.

Uses PyMySQL with DictCursor so query results come back as dictionaries,
which map cleanly onto the Jinja2 templates (e.g. txn.date, txn.amount).
"""

import os
import logging
from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

logger = logging.getLogger(__name__)

_pool = None


def init_pool(app=None):
    """
    Initialize the global connection pool. Call once at application startup
    (e.g. from app.py's create_app()).
    """
    global _pool
    if _pool is not None:
        return _pool

    config = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": int(os.environ.get("DB_PORT", 3306)),
        "user": os.environ.get("DB_USER", "root"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "database": os.environ.get("DB_NAME", "finance_coach"),
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
        "autocommit": False,
    }

    _pool = PooledDB(
        creator=pymysql,
        maxconnections=int(os.environ.get("DB_POOL_SIZE", 10)),
        mincached=2,
        maxcached=5,
        blocking=True,
        ping=1,  # ping connection before use, reconnect if stale
        **config,
    )
    logger.info("Database connection pool initialized")
    return _pool


def get_pool():
    if _pool is None:
        raise RuntimeError("Connection pool not initialized. Call init_pool() first.")
    return _pool


@contextmanager
def get_connection():
    """Yield a pooled connection, returning it to the pool afterwards."""
    conn = get_pool().connection()
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_cursor(commit=False):
    """
    Yield a (connection, cursor) pair. If commit=True, commits on success
    and rolls back on exception.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield conn, cursor
            if commit:
                conn.commit()
        except Exception:
            if commit:
                conn.rollback()
            raise
        finally:
            cursor.close()


def fetch_one(query, params=None):
    with get_cursor() as (conn, cursor):
        cursor.execute(query, params or ())
        return cursor.fetchone()


def fetch_all(query, params=None):
    with get_cursor() as (conn, cursor):
        cursor.execute(query, params or ())
        return cursor.fetchall()


def execute(query, params=None):
    """For INSERT/UPDATE/DELETE. Returns lastrowid (useful for INSERTs)."""
    with get_cursor(commit=True) as (conn, cursor):
        cursor.execute(query, params or ())
        return cursor.lastrowid


def execute_many(query, param_list):
    with get_cursor(commit=True) as (conn, cursor):
        cursor.executemany(query, param_list)
        return cursor.rowcount


def call_procedure(proc_name, params=None):
    """Call a stored procedure (e.g. sp_get_monthly_summary) and return all result sets."""
    with get_cursor() as (conn, cursor):
        cursor.callproc(proc_name, params or ())
        results = cursor.fetchall()
        return results