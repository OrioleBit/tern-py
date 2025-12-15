from dataclasses import dataclass

from order_app.domain.entities.user import UserRole
from order_app.domain.repositories import OrderRepository, ProductRepository


@dataclass
class EditOrderRequest:
    order_id: str
    user_id: str
    role: UserRole
    product_id: str
    quantity: int


@dataclass
class EditOrderUseCase:
    order_repository: OrderRepository
    product_repository: ProductRepository

    def execute(self, request: EditOrderRequest) -> None:
        order = self.order_repository.get_by_id(request.order_id)
        if not order:
            raise ValueError(f"Order with ID {request.order_id} not found")

        product = self.product_repository.get_by_id(request.product_id)
        if not product:
            raise ValueError(f"Product with ID {request.product_id} not found")

        if request.role != UserRole.MANAGER and order.user_id != request.user_id:
            raise ValueError("You don't have permission to edit this order")

        order.edit_item(request.product_id, request.quantity)
        self.order_repository.save(order)
