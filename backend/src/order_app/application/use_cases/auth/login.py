from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.login import (
    LoginUserRequestDto,
    LoginUserResponseDto,
)
from order_app.application.ports.jwt_service import AuthTokenService
from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories.auth.refresh_token_repository import (
    RefreshTokenRepository,
)
from order_app.application.repositories.user_repository import UserRepository
from order_app.domain.entities.auth.refresh_token import RefreshToken
from order_app.domain.exceptions import UserNotFoundError


@dataclass
class LoginUserUseCase:
    user_repository: UserRepository
    password_hasher: PasswordHasher
    auth_token_service: AuthTokenService
    refresh_token_repo: RefreshTokenRepository

    def execute(self, request: LoginUserRequestDto) -> Result[LoginUserResponseDto]:
        try:
            user = self.user_repository.get_by_email(email=request.email)
        except UserNotFoundError:
            return Result.failure(Error.domain("Invalid credentials"))

        verify_result = self.password_hasher.verify(
            plain_password=request.password, hashed_password=user.password_hash
        )
        if not verify_result:
            return Result.failure(Error.domain("Invalid credentials"))

        access_token = self.auth_token_service.generate_token(
            payload={"sub": str(user.id), "role": user.role.name}, expires_in=3600
        )
        refresh_token_str = self.auth_token_service.generate_token(
            payload={"sub": str(user.id), "role": user.role.name},
            expires_in=7 * 24 * 3600,
        )
        refresh_token = RefreshToken.new(
            user_id=user.id, token=refresh_token_str, expires_at=7 * 24 * 3600
        )
        self.refresh_token_repo.save(refresh_token=refresh_token)

        return Result.success(
            LoginUserResponseDto(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                access_token=access_token,
                refresh_token=refresh_token_str,
            )
        )
