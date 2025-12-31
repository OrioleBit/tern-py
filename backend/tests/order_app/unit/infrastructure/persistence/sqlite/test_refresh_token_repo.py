import sqlite3
from uuid import UUID
from weakref import ref

import pytest
from order_app.domain.entities.auth.refresh_token import RefreshToken
from order_app.domain.exceptions.token_errors import RefreshTokenNotFoundError
from order_app.infrastructure.persistence.sqlite.refresh_token_repo import (
    SqliteRefreshTokenRepository,
)


def get_connection():
    conn = sqlite3.connect(":memory:")
    return conn


def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()

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


def test_get_token_by_id():
    conn = get_connection()
    init_db(conn)
    repo = SqliteRefreshTokenRepository(connection=conn)

    repo.save(
        refresh_token=RefreshToken.new(
            token="token", user_id="user_id", expires_at=1, is_revoked=False
        ),
    )

    fetched_token = repo.get_by_token(token="token")
    assert fetched_token.token == "token"
    assert fetched_token.user_id == "user_id"
    assert not fetched_token.is_revoked
    assert fetched_token.expires_at == 1


def test_get_token_by_id_does_not_exist():
    conn = get_connection()
    init_db(conn)
    repo = SqliteRefreshTokenRepository(connection=conn)

    with pytest.raises(RefreshTokenNotFoundError):
        repo.get_by_token(token="token")


def test_revoke_token():
    conn = get_connection()
    init_db(conn)
    repo = SqliteRefreshTokenRepository(connection=conn)

    refresh_token = RefreshToken.new(
        token="token", user_id="user_id", expires_at=1, is_revoked=False
    )
    repo.save(refresh_token=refresh_token)

    repo.revoke_token(token_id=str(refresh_token.id))

    fetched_token = repo.get_by_token(token="token")
    assert fetched_token.is_revoked


def test_save_new_object():
    conn = get_connection()
    init_db(conn)
    repo = SqliteRefreshTokenRepository(connection=conn)

    repo.save(
        refresh_token=RefreshToken.new(
            token="token", user_id="user_id", expires_at=1, is_revoked=False
        ),
    )

    fetched_token = repo.get_by_token(token="token")
    assert fetched_token.token == "token"
    assert fetched_token.user_id == "user_id"
    assert not fetched_token.is_revoked
    assert fetched_token.expires_at == 1


def test_save_object_already_exists():
    conn = get_connection()
    init_db(conn)
    repo = SqliteRefreshTokenRepository(connection=conn)

    refresh_token = RefreshToken.new(
        token="token", user_id="user_id", expires_at=1, is_revoked=False
    )
    repo.save(refresh_token=refresh_token)

    repo.save(
        refresh_token=RefreshToken.from_existing(
            id=refresh_token.id,
            token="token_edited",
            user_id="user_id_edited",
            expires_at=10,
            is_revoked=True,
        ),
    )

    fetched_token = repo.get_by_token(token="token_edited")
    assert fetched_token.token == "token_edited"
    assert UUID(fetched_token.id) == refresh_token.id
    assert fetched_token.user_id == "user_id_edited"
    assert fetched_token.is_revoked
    assert fetched_token.expires_at == 10
