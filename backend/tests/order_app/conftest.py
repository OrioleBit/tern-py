from unittest.mock import MagicMock

import pytest
from order_app.application.repositories.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from order_app.domain.entities.auth.refresh_token import RefreshToken


# Application-level fixtures
@pytest.fixture
def register_user_use_case(user_repository):
    class MockRegisterUserUseCase:
        def __init__(self):
            self.execute = MagicMock()
            self.user_repository = user_repository

    return MockRegisterUserUseCase()


# Domain-level fixtures
@pytest.fixture
def user_repository():
    class MockUserRepository:
        def __init__(self):
            self.create = MagicMock()
            self.get_by_id = MagicMock()
            self.get_by_email = MagicMock()

    return MockUserRepository()


@pytest.fixture
def order_repository():
    class MockOrderRepository:
        def __init__(self):
            self.create = MagicMock()
            self.update = MagicMock()
            self.delete = MagicMock()
            self.get_by_id = MagicMock()
            self.get_list = MagicMock()

    return MockOrderRepository()


@pytest.fixture
def product_repository():
    class MockProductRepository:
        def __init__(self):
            self.create = MagicMock()
            self.update = MagicMock()
            self.get_by_id = MagicMock()

    return MockProductRepository()


@pytest.fixture
def refresh_token_repo():
    class MockRefreshTokenRepository(RefreshTokenRepository):
        def save(self, refresh_token: RefreshToken):
            pass

        def get_by_token(self, token: str) -> RefreshToken:
            return "refresh_token"

        def revoke_token(self, token_id: str):
            pass

    return MockRefreshTokenRepository
