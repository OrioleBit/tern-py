import datetime
from dataclasses import dataclass, field
from decimal import Decimal
from functools import reduce
from uuid import UUID

from order_app.domain.value_objects import Money, OrderItem
from order_app.domain.value_objects.order_status import OrderStatus

from .entity import Entity
from .product import Product


@dataclass
class Order(Entity):
    user_id: UUID
    _items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now()
    )
    updated_at: datetime.datetime | None = None

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
            unit_price=product.price,
        )
        self._items.append(item)
        self.updated_at = datetime.datetime.now()

    def load_items(self, items: list[tuple[Product, int]]):
        for item in items:
            item = OrderItem(
                product_id=item[0].id,
                quantity=item[1],
                unit_price=item[0].price,
            )
            self._items.append(item)

    def get_items(self):
        return self._items

    def remove_item(self, order_item: OrderItem) -> None:
        if order_item in self._items:
            self._items.remove(order_item)
            self.updated_at = datetime.datetime.now()

    def edit_item(self, product: Product, new_quantity: int) -> None:
        for item in self._items:
            if item.product_id == product.id:
                old_quantity = item.quantity
                delta = new_quantity - old_quantity
                if delta > 0:
                    product.decrease_stock(delta)
                elif delta < 0:
                    product.increase_stock(-delta)
                item.quantity = new_quantity
                self.updated_at = datetime.datetime.now()
                break

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def item_count(self) -> int:
        return len(self._items)
