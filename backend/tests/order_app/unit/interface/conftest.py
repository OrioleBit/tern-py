from unittest.mock import MagicMock

import pytest
from order_app.application.use_cases.auth.login import LoginUserUseCase


@pytest.fixture
def register_user_use_case(user_repository):
    class MockRegisterUserUseCase:
        def __init__(self):
            self.execute = MagicMock()
            self.user_repository = user_repository

    return MockRegisterUserUseCase()


@pytest.fixture
def login_user_use_case(user_repository, password_hasher, auth_token_service):
    class MockLoginUserUseCase(LoginUserUseCase):
        def __init__(self):
            self.execute = MagicMock()
            self.user_repository = user_repository
            self.password_hasher = password_hasher
            self.auth_token_service = auth_token_service

    return MockLoginUserUseCase()
