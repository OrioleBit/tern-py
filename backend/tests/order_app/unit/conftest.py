from dataclasses import dataclass

import pytest
from order_app.application.ports.jwt_service import AuthTokenService
from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from order_app.domain.entities.auth.refresh_token import RefreshToken


@pytest.fixture
def password_hasher():
    class MockPasswordHasher(PasswordHasher):
        def hash(self, plain_password: str) -> str:
            return "password_hash"

        def verify(self, plain_password: str, hashed_password: str) -> bool:
            return plain_password == hashed_password

    return MockPasswordHasher()


@pytest.fixture
def auth_token_service():
    @dataclass
    class MockAuthTokenService(AuthTokenService):
        def generate_token(self, payload: dict, expires_in: int = None) -> str:
            return "simple_token"

        def verify_token(self, token: str) -> dict:
            return {"sub": "user_id", "role": "user_role"}

    return MockAuthTokenService(secret_key="secret_key", algorithm="HS256")
