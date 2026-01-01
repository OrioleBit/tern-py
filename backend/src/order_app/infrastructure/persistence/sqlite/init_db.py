import sqlite3


def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS refresh_tokens (
            id TEXT PRIMARY KEY,
            token TEXT NOT NULL,
            user_id TEXT NOT NULL,
            expires_at INTEGER NOT NULL,
            is_revoked BOOLEAN NOT NULL
        )"""
    )
    conn.commit()
