import datetime
from dataclasses import dataclass, field

from order_app.domain.exceptions import InsufficientStockError
from order_app.domain.value_objects.money import Money

from .entity import Entity


@dataclass
class Product(Entity):
    name: str
    description: str
    price: Money
    stock_quantity: int
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now()
    )
    updated_at: datetime.datetime | None = None

    def decrease_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > self.stock_quantity:
            raise InsufficientStockError(
                f"Insufficient stock to decrease: requested {quantity}, available {self.stock_quantity}"
            )
        self.stock_quantity -= quantity
        self.updated_at = datetime.datetime.now()

    def increase_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.stock_quantity += quantity
        self.updated_at = datetime.datetime.now()
