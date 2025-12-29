from unittest.mock import MagicMock

from freezegun import freeze_time
from order_app.application.common.result import Error, ErrorCode
from order_app.application.dtos.user.register import (
    RegisterUserRequestDto,
    RegisterUserResponseDto,
    TokensResponseDto,
    UserResponseDto,
)
from order_app.application.use_cases.user import RegisterUserUseCase
from order_app.domain.exceptions import UserNotFoundError
from order_app.domain.value_objects.user_role import UserRole


def test_register_user_found_by_email(
    user_repository, auth_token_service, refresh_token_repo
):
    use_case = RegisterUserUseCase(
        user_repository=user_repository,
        password_hasher=None,
        auth_token_service=auth_token_service,
        refresh_token_repo=refresh_token_repo,
    )
    request = RegisterUserRequestDto(name="name", email="email", password="password")

    result = use_case.execute(request)

    use_case.user_repository.get_by_email.assert_called_once_with(request.email)

    assert not result.is_success
    assert result.error == Error(
        code=ErrorCode.ALREADY_EXISTS,
        message="User already exists",
        details={"attr_name": "email", "attr_value": request.email},
    )


@freeze_time("2022-01-01")
def test_register_user(
    user_repository, password_hasher, auth_token_service, refresh_token_repo
):
    user_repository.get_by_email.side_effect = UserNotFoundError
    user_repository.create = MagicMock()
    auth_token_service.generate_token = MagicMock()
    auth_token_service.generate_token.side_effect = [
        "access_token_123",
        "refresh_token_456",
    ]
    refresh_token_repo.save = MagicMock()
    use_case = RegisterUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        auth_token_service=auth_token_service,
        refresh_token_repo=refresh_token_repo,
    )
    request = RegisterUserRequestDto(name="name", email="email", password="password")

    result = use_case.execute(request)

    new_user = user_repository.create.call_args.kwargs["user"]
    new_user.name == request.name
    new_user.email == request.email
    new_user.password_hash == password_hasher.hash(request.password)
    new_user.role == UserRole.CUSTOMER

    refresh_token = refresh_token_repo.save.call_args.kwargs["refresh_token"]
    assert refresh_token.user_id == new_user.id
    assert refresh_token.token == "refresh_token_456"
    assert refresh_token.expires_at == 7 * 24 * 3600
    assert not refresh_token.is_revoked

    assert result.is_success
    assert result.value == RegisterUserResponseDto(
        user=UserResponseDto(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            role=new_user.role.value,
        ),
        tokens=TokensResponseDto(
            access_token="access_token_123", refresh_token="refresh_token_456"
        ),
    )
