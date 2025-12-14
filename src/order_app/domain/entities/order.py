from dataclasses import dataclass, field
import datetime
from enum import auto
from typing import Optional
from uuid import UUID
from .entity import Entity
from decimal import Decimal


from .product import Product


class OrderStatus:
    CREATED = auto()
    PAID = auto()
    FULFILLING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price_per_unit: Decimal

    def total_price(self) -> Decimal:
        return self.price_per_unit * self.quantity

    def __str__(self):
        return (
            f"OrderItem(product_id={self.product_id}, quantity={self.quantity}, "
            f"price_per_unit={self.price_per_unit})"
        )


@dataclass
class Order(Entity):
    user_id: UUID
    _items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: Optional[datetime.datetime] = None

    @property
    def total_price(self) -> Decimal:
        return sum(item.total_price() for item in self._items)

    def add_item(self, product: Product, quantity: int) -> None:
        product.decrease_stock(quantity)
        item = OrderItem(
            product_id=product.id,
            quantity=quantity,
            price_per_unit=product.price,
        )
        self._items.append(item)
        self.updated_at = datetime.datetime.now()

    def remove_item(self, order_item: OrderItem) -> None:
        raise NotImplementedError("remove_item method is not implemented yet.")

    def clear_items(self) -> None:
        raise NotImplementedError("clear_items method is not implemented yet.")

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def item_count(self) -> int:
        return len(self._items)

    def __str__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, items:[{', '.join(str(item) for item in self._items)}])"
