from unittest.mock import MagicMock
from uuid import uuid4

from freezegun import freeze_time

from order_app.application.common.result import ErrorCode
from order_app.application.dtos.user.login import (
    LoginUserRequestDto,
    LoginUserResponseDto,
)
from order_app.application.use_cases.user.login import LoginUserUseCase
from order_app.domain.entities.user import User
from order_app.domain.exceptions import UserNotFoundError
from order_app.domain.value_objects.user_role import UserRole


def test_login_user_user_not_found(user_repository, password_hasher, jwt_service):
    user_repository.get_by_email.side_effect = [UserNotFoundError]
    password_hasher.verify = MagicMock()
    jwt_service.generate_token = MagicMock()
    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_not_called()
    jwt_service.generate_token.assert_not_called()
    assert not result.is_success
    assert result.error.code == ErrorCode.DOMAIN
    assert result.error.message == "Invalid credentials"


def test_login_user_invalid_password(user_repository, password_hasher, jwt_service):
    user_repository.get_by_email.return_value.password_hash = "hashed_password"
    password_hasher.verify = MagicMock(return_value=False)
    jwt_service.generate_token = MagicMock()
    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_called_once_with(
        plain_password="password", hashed_password="hashed_password"
    )
    jwt_service.generate_token.assert_not_called()
    assert not result.is_success
    assert result.error.code == ErrorCode.DOMAIN
    assert result.error.message == "Invalid credentials"


@freeze_time("2022-01-01")
def test_login_user(user_repository, password_hasher, jwt_service):
    user = User.from_existing(
        id=uuid4(),
        name="Test User",
        email="email@test.com",
        password_hash="hashed_password",
        role=UserRole.CUSTOMER,
    )

    user_repository.get_by_email.return_value = user
    password_hasher.verify = MagicMock(return_value=True)
    jwt_service.generate_token = MagicMock(return_value="simple_token")

    use_case = LoginUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )

    result = use_case.execute(
        LoginUserRequestDto(email="email@test.com", password="password")
    )

    user_repository.get_by_email.assert_called_once_with(email="email@test.com")
    password_hasher.verify.assert_called_once_with(
        plain_password="password", hashed_password="hashed_password"
    )
    jwt_service.generate_token.assert_called_once_with(
        payload={"sub": str(user.id), "role": user.role.name}
    )
    assert result.is_success
    assert result.value == LoginUserResponseDto(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        access_token="simple_token",
        expires_in=jwt_service.expires_in,
    )
