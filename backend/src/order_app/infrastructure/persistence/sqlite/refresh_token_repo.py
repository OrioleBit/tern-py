import sqlite3
from dataclasses import dataclass

from order_app.application.repositories.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from order_app.domain.entities.auth.refresh_token import RefreshToken
from order_app.domain.exceptions.token_errors import RefreshTokenNotFoundError


@dataclass
class SqliteRefreshTokenRepository(RefreshTokenRepository):
    connection: sqlite3.Connection

    def save(self, refresh_token: RefreshToken):
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
            INSERT INTO refresh_tokens (id, user_id, token, expires_at, is_revoked)
            VALUES (?, ?, ?, ?, ?)
            """,
                (
                    str(refresh_token.id),
                    str(refresh_token.user_id),
                    refresh_token.token,
                    refresh_token.expires_at,
                    refresh_token.is_revoked,
                ),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            cursor.execute(
                """
                UPDATE refresh_tokens
                SET token = ?, expires_at = ?, is_revoked = ?, user_id = ?
                WHERE id = ?
                """,
                (
                    refresh_token.token,
                    refresh_token.expires_at,
                    refresh_token.is_revoked,
                    str(refresh_token.user_id),
                    str(refresh_token.id),
                ),
            )
            self.connection.commit()

    def get_by_token(self, token: str) -> RefreshToken:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, token, expires_at, is_revoked
            FROM refresh_tokens
            WHERE token = ?
            """,
            (token,),
        )
        row = cursor.fetchone()
        if not row:
            raise RefreshTokenNotFoundError
        return RefreshToken(
            id=row[0],
            user_id=row[1],
            token=row[2],
            expires_at=row[3],
            is_revoked=row[4],
        )

    def revoke_token(self, token_id: str):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE refresh_tokens
            SET is_revoked = 1
            WHERE id = ?
            """,
            (token_id,),
        )
        self.connection.commit()
