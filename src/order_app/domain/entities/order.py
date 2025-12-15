import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from enum import auto
from functools import reduce
from typing import Optional
from uuid import UUID

from order_app.domain.value_objects.money import Money

from .entity import Entity
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
    price_per_unit: Money

    def total_price(self) -> Money:
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
    def total_price(self) -> Money:
        return reduce(
            lambda x, y: x + y,
            [item.total_price() for item in self._items],
            Money(Decimal("0")),
        )

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
        if order_item in self._items:
            self._items.remove(order_item)
            self.updated_at = datetime.datetime.now()

    def edit_item(self, product_id: str, quantity: int) -> None:
        for item in self._items:
            if item.product_id == product_id:
                item.quantity = quantity
                self.updated_at = datetime.datetime.now()
                break

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def item_count(self) -> int:
        return len(self._items)

    def __str__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, items:[{', '.join(str(item) for item in self._items)}])"
