import sqlite3

from order_app.infrastructure.persistence.sqlite.init_db import init_db


def test_init_db_creates_tables():
    conn = sqlite3.connect(":memory:")

    init_db(conn=conn)

    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    assert "users" in tables
    assert "refresh_tokens" in tables

    cursor.execute("PRAGMA table_info(users);")
    columns = [row[1] for row in cursor.fetchall()]
    expected_columns = ["id", "name", "email", "password_hash", "role"]
    for col in expected_columns:
        assert col in columns

    cursor.execute("PRAGMA table_info(refresh_tokens);")
    columns = [row[1] for row in cursor.fetchall()]
    expected_columns = ["id", "token", "user_id", "expires_at", "is_revoked"]
    for col in expected_columns:
        assert col in columns

    conn.close()
