from dataclasses import dataclass

from .money import Money


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: Money

    def total_price(self) -> Money:
        return self.unit_price * self.quantity
