from enum import Enum, auto

from order_app.domain.exceptions import InvalidUserRoleError


class UserRole(Enum):
    MANAGER = auto()
    CUSTOMER = auto()
    ADMIN = auto()

    @classmethod
    def from_str(cls, role: str):
        try:
            return cls[role.upper()]
        except (KeyError, AttributeError):
            raise InvalidUserRoleError(role)
