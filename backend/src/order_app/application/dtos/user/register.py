from dataclasses import dataclass
from typing import Self
from uuid import UUID

from order_app.domain.entities.user import User


@dataclass
class RegisterUserRequestDto:
    name: str
    email: str
    password: str


@dataclass
class UserResponse:
    id: UUID
    name: str
    email: str
    role: str

    @classmethod
    def from_entity(cls, user: User) -> Self:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role.value,
        )
