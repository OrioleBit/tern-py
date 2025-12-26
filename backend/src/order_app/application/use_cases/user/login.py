from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.user.login import (
    LoginUserRequestDto,
    LoginUserResponseDto,
)
from order_app.application.ports.jwt_service import JwtService
from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories.user_repository import UserRepository
from order_app.domain.exceptions import UserNotFoundError


@dataclass
class LoginUserUseCase:
    user_repository: UserRepository
    password_hasher: PasswordHasher
    jwt_service: JwtService

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

        access_token = self.jwt_service.generate_token(
            payload={"sub": str(user.id), "role": user.role.name}
        )

        return Result.success(
            LoginUserResponseDto(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role,
                access_token=access_token,
                expires_in=self.jwt_service.expires_in,
            )
        )
