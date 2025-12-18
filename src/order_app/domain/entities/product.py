import datetime
from dataclasses import dataclass, field
from typing import Optional

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
    updated_at: Optional[datetime.datetime] = None

    # def __str__(self) -> str:
    #     return f"Product(id={self.id}, name={self.name}, price={self.price}, stock_quantity={self.stock_quantity})"

    def decrease_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if quantity > self.stock_quantity:
            raise ValueError(
                "Insufficient stock to decrease: requested {quantity}, available {self.stock_quantity}"
            )
        self.stock_quantity -= quantity
        self.updated_at = datetime.datetime.now()
