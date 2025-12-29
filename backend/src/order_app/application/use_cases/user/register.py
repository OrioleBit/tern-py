from dataclasses import dataclass
from math import exp

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.register import (
    RegisterUserRequestDto,
    RegisterUserResponseDto,
    TokensResponseDto,
    UserResponseDto,
)
from order_app.application.ports.auth_token_service import AuthTokenService
from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from order_app.application.repositories.user_repository import UserRepository
from order_app.domain.entities.auth.refresh_token import RefreshToken
from order_app.domain.entities.user import User
from order_app.domain.exceptions import UserNotFoundError


@dataclass
class RegisterUserUseCase:
    user_repository: UserRepository
    password_hasher: PasswordHasher
    auth_token_service: AuthTokenService
    refresh_token_repo: RefreshTokenRepository

    def execute(
        self, request: RegisterUserRequestDto
    ) -> Result[RegisterUserResponseDto]:
        try:
            self.user_repository.get_by_email(request.email)
        except UserNotFoundError:
            password_hash = self.password_hasher.hash(request.password)
            user = User.new(
                name=request.name,
                email=request.email,
                password_hash=password_hash,
            )

            self.user_repository.create(user=user)
            access_token = self.auth_token_service.generate_token(
                payload={"sub": str(user.id), "role": user.role.name}, expires_in=3600
            )
            refresh_token_str = self.auth_token_service.generate_token(
                payload={"sub": str(user.id), "role": user.role.name},
                expires_in=7 * 24 * 3600,
            )
            refresh_token = RefreshToken.new(
                user_id=user.id,
                token=refresh_token_str,
                expires_at=7 * 24 * 3600,
            )
            self.refresh_token_repo.save(refresh_token=refresh_token)
            return Result.success(
                RegisterUserResponseDto(
                    user=UserResponseDto.from_entity(user),
                    tokens=TokensResponseDto(
                        access_token=access_token, refresh_token=refresh_token_str
                    ),
                )
            )

        else:
            return Result.failure(
                Error.already_exists(
                    entity="User", attr_name="email", attr_value=request.email
                )
            )
