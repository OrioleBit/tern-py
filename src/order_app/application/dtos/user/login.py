from dataclasses import dataclass
from uuid import UUID

from order_app.domain.value_objects.user_role import UserRole


@dataclass(frozen=True)
class LoginUserRequestDto:
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserResponseDto:
    id: UUID
    name: str
    email: str
    role: UserRole
    access_token: str
    expires_in: str
