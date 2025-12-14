from dataclasses import dataclass
from uuid import UUID

from order_app.domain.entities.order import Order
from order_app.domain.repositories import product_repository
from order_app.domain.repositories.order_repository import OrderRepository


@dataclass
class ItemRequest:
    product_id: UUID
    quantity: int


@dataclass
class CreateOrderRequest:
    user_id: UUID
    items: list[ItemRequest]


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepository
    product_repository: product_repository.ProductRepository

    def execute(self, request: CreateOrderRequest) -> Order:
        order = Order(user_id=request.user_id)

        for item in request.items:
            product_id = item.product_id
            product = self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")

            order.add_item(product, item.quantity)
            self.product_repository.update(product)
        self.order_repository.save(order)
        return order
