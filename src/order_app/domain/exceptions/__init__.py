__all__ = [
    "InvalidTokenError",
    "TokenExpiredError",
    "UserNotFoundError",
    "UserAlreadyExistsError",
    "OrderNotFoundError",
    "ProductNotFoundError",
    "InsufficientStockError",
    "InvalidUserRoleError",
]


from uuid import UUID

from order_app.domain.exceptions.base import DomainError
from order_app.domain.exceptions.token_errors import (
    InvalidTokenError,
    TokenExpiredError,
)


class UserNotFoundError(DomainError):
    def __init__(self, user_id: UUID | None = None, email: str | None = None):
        self.user_id = user_id
        self.email = email
        super().__init__("User not found")


class UserAlreadyExistsError(DomainError):
    def __init__(self, user_id: UUID | None = None, email: str | None = None):
        self.user_id = user_id
        self.email = email
        super().__init__("User already exists")


class OrderNotFoundError(DomainError):
    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} not found")


class ProductNotFoundError(DomainError):
    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Product with ID {order_id} not found")


class InsufficientStockError(DomainError):
    def __init__(self, product_id: UUID):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} is out of stock")


class InvalidUserRoleError(DomainError):
    def __init__(self, role: str):
        self.role = role
        super().__init__(f"Invalid user role: {role}")
