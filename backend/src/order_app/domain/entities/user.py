import datetime
from dataclasses import dataclass, field

from order_app.domain.value_objects import UserRole

from .entity import Entity


@dataclass
class User(Entity):
    name: str
    email: str
    password_hash: str
    role: UserRole = field(default_factory=lambda: UserRole.CUSTOMER)
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now()
    )
    updated_at: datetime.datetime | None = None

    def update_role(self, role: UserRole) -> None:
        self.role = role
        self.updated_at = datetime.datetime.now()

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def is_manager(self) -> bool:
        return self.role == UserRole.MANAGER

    @property
    def is_customer(self) -> bool:
        return self.role == UserRole.CUSTOMER
