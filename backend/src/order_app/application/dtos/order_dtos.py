from dataclasses import dataclass
from typing import Self
from uuid import UUID

from order_app.domain.entities.order import Order
from order_app.domain.entities.user import UserRole


@dataclass
class ItemRequest:
    product_id: UUID
    quantity: int


@dataclass
class CreateOrderRequest:
    user_id: UUID
    items: list[ItemRequest]


@dataclass
class DeleteOrderRequest:
    order_id: UUID
    user_id: UUID
    role: UserRole


@dataclass
class EditOrderRequest:
    order_id: str
    user_id: str
    role: UserRole
    product_id: str
    quantity: int


@dataclass
class ListOrderRequest:
    user_id: UUID
    role: UserRole


@dataclass
class OrderResponse:
    order_id: UUID
    user_id: UUID
    status: str
    items: list[dict]
    total_price: str
    item_count: int
    created_at: str
    updated_at: str | None

    @classmethod
    def from_entity(cls, order: Order) -> Self:
        return cls(
            order_id=order.id,
            user_id=order.user_id,
            status=order.status.value,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                }
                for item in order._items
            ],
            total_price=str(order.total_price),
            item_count=order.item_count,
            created_at=str(order.created_at),
            updated_at=str(order.updated_at),
        )
