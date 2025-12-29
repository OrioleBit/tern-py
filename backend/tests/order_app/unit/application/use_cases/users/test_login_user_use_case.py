import re
from math import exp
from unittest.mock import ANY, MagicMock, call
from uuid import uuid4

from freezegun import freeze_time
from order_app.application.common.result import ErrorCode
from order_app.application.dtos.user.login import (
    LoginUserRequestDto,
    LoginUserResponseDto,
)
from order_app.application.use_cases.auth.login import LoginUserUseCase
from order_app.domain.entities.auth.refresh_token import RefreshToken
from order_app.domain.entities.user import User
from order_app.domain.exceptions import UserNotFoundError
from order_app.domain.value_objects.user_role import UserRole


def test_login_user_user_not_found(
    user_repository, password_hasher, auth_token_service, refresh_token_repo
):
    user_repository.get_by_email.side_effect = [UserNotFoundError]
    password_hasher.verify = MagicMock()
    auth_token_service.generate_token = MagicMock()
    refresh_token_repo.save = MagicMock()
    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        auth_token_service=auth_token_service,
        refresh_token_repo=refresh_token_repo,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_not_called()
    auth_token_service.generate_token.assert_not_called()
    refresh_token_repo.save.assert_not_called()
    assert not result.is_success
    assert result.error.code == ErrorCode.DOMAIN
    assert result.error.message == "Invalid credentials"


def test_login_user_invalid_password(
    user_repository, password_hasher, auth_token_service, refresh_token_repo
):
    user_repository.get_by_email.return_value.password_hash = "hashed_password"
    password_hasher.verify = MagicMock(return_value=False)
    auth_token_service.generate_token = MagicMock()
    refresh_token_repo.save = MagicMock()
    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        auth_token_service=auth_token_service,
        refresh_token_repo=refresh_token_repo,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_called_once_with(
        plain_password="password", hashed_password="hashed_password"
    )
    auth_token_service.generate_token.assert_not_called()
    refresh_token_repo.save.assert_not_called()
    assert not result.is_success
    assert result.error.code == ErrorCode.DOMAIN
    assert result.error.message == "Invalid credentials"


@freeze_time("2022-01-01")
def test_login_user(
    user_repository, password_hasher, auth_token_service, refresh_token_repo
):
    user = User.from_existing(
        id=uuid4(),
        name="Test User",
        email="email@test.com",
        password_hash="hashed_password",
        role=UserRole.CUSTOMER,
    )

    user_repository.get_by_email.return_value = user
    password_hasher.verify = MagicMock(return_value=True)
    auth_token_service.generate_token = MagicMock()
    auth_token_service.generate_token.side_effect = [
        "access_token_123",
        "refresh_token_456",
    ]
    refresh_token_repo.save = MagicMock()

    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        auth_token_service=auth_token_service,
        refresh_token_repo=refresh_token_repo,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_called_once_with(
        plain_password="password", hashed_password="hashed_password"
    )

    saved_refresh_token = refresh_token_repo.save.call_args.kwargs["refresh_token"]
    assert saved_refresh_token.user_id == user.id
    assert not saved_refresh_token.is_revoked
    assert saved_refresh_token.token == "refresh_token_456"
    assert saved_refresh_token.expires_at == 7 * 24 * 3600

    assert result.is_success
    assert result.value == LoginUserResponseDto(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        access_token="access_token_123",
        refresh_token="refresh_token_456",
    )
