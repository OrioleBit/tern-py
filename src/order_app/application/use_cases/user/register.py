from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.register import (
    RegisterUserRequestDto,
    UserResponse,
)
from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories.user_repository import UserRepository
from order_app.domain.entities.user import User
from order_app.domain.exceptions import UserNotFoundError


@dataclass
class RegisterUserUseCase:
    user_repository: UserRepository
    password_hasher: PasswordHasher

    def execute(self, request: RegisterUserRequestDto) -> Result[User]:
        try:
            self.user_repository.get_by_email(request.email)
        except UserNotFoundError:
            password_hash = self.password_hasher.hash(request.password)
            user = User.new(
                name=request.name,
                email=request.email,
                password_hash=password_hash,
            )

            self.user_repository.create(user)
            return Result.success(UserResponse.from_entity(user))
        else:
            return Result.failure(
                Error.already_exists(
                    entity="User", attr_name="email", attr_value=request.email
                )
            )
