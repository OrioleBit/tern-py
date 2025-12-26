from freezegun import freeze_time

from order_app.application.common.result import Error, ErrorCode
from order_app.application.dtos.user.register import (
    RegisterUserRequestDto,
    UserResponse,
)
from order_app.application.use_cases.user import RegisterUserUseCase
from order_app.domain.entities.user import User
from order_app.domain.exceptions import UserNotFoundError
from order_app.domain.value_objects.user_role import UserRole


def test_register_user_found_by_email(user_repository):
    use_case = RegisterUserUseCase(
        user_repository=user_repository, password_hasher=None
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
def test_register_user(user_repository, password_hasher):
    user_repository.get_by_email.side_effect = UserNotFoundError
    use_case = RegisterUserUseCase(
        user_repository=user_repository, password_hasher=password_hasher
    )
    request = RegisterUserRequestDto(name="name", email="email", password="password")

    result = use_case.execute(request)

    desired_user = User.new(
        name=request.name,
        email=request.email,
        password_hash=password_hasher.hash(request.password),
        role=UserRole.CUSTOMER,
    )

    desired_user.id = result.value.id
    user_repository.get_by_email.assert_called_once_with(request.email)
    user_repository.create.assert_called_once_with(desired_user)

    assert result.is_success
    assert result.value == UserResponse.from_entity(desired_user)
    assert result.value == UserResponse.from_entity(desired_user)
    assert result.is_success
    assert result.value == UserResponse.from_entity(desired_user)
    assert result.value == UserResponse.from_entity(desired_user)
