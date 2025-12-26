from dataclasses import dataclass

import pytest

from order_app.application.ports.jwt_service import JwtService
from order_app.application.ports.password_hasher import PasswordHasher


@pytest.fixture
def password_hasher():
    class MockPasswordHasher(PasswordHasher):
        def hash(self, plain_password: str) -> str:
            return "password_hash"

        def verify(self, plain_password: str, hashed_password: str) -> bool:
            return plain_password == hashed_password

    return MockPasswordHasher()


@pytest.fixture
def jwt_service():
    @dataclass
    class MockJwtService(JwtService):
        def generate_token(self, payload) -> str:
            return "simple_token"

        def verify_token(self, token) -> dict:
            return {"sub": "user_id", "role": "user_role"}

    return MockJwtService(secret_key="secret_key", algorithm="HS256", expires_in=3600)
