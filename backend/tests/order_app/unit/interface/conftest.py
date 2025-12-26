from unittest.mock import MagicMock

import pytest

from order_app.application.use_cases.user.login import LoginUserUseCase


@pytest.fixture
def register_user_use_case(user_repository):
    class MockRegisterUserUseCase:
        def __init__(self):
            self.execute = MagicMock()
            self.user_repository = user_repository

    return MockRegisterUserUseCase()


@pytest.fixture
def login_user_use_case(user_repository, password_hasher, jwt_service):
    class MockLoginUserUseCase(LoginUserUseCase):
        def __init__(self):
            self.execute = MagicMock()
            self.user_repository = user_repository
            self.password_hasher = password_hasher
            self.jwt_service = jwt_service

    return MockLoginUserUseCase()
