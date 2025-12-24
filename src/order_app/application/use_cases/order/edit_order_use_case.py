from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.order_dtos import EditOrderRequest, OrderResponse
from order_app.application.repositories import OrderRepository, ProductRepository
from order_app.domain.entities.user import UserRole
from order_app.domain.exceptions import OrderNotFoundError, ProductNotFoundError


@dataclass
class EditOrderUseCase:
    order_repository: OrderRepository
    product_repository: ProductRepository

    def execute(self, request: EditOrderRequest) -> Result[OrderResponse]:
        try:
            order = self.order_repository.get_by_id(request.order_id)
        except OrderNotFoundError:
            return Result.failure(
                Error.not_found(
                    entity="Order", attr_name="id", attr_value=str(request.order_id)
                )
            )

        try:
            product = self.product_repository.get_by_id(request.product_id)
        except ProductNotFoundError:
            return Result.failure(
                Error.not_found(
                    entity="Product", attr_name="id", attr_value=str(request.product_id)
                )
            )

        if request.role != UserRole.MANAGER and order.user_id != request.user_id:
            return Result.failure(
                Error.forbidden(
                    entity="Order", action="edit", entity_id=str(request.order_id)
                )
            )

        order.edit_item(product, request.quantity)
        self.product_repository.update(product)
        self.order_repository.update(order)
        return Result.success(OrderResponse.from_entity(order))
