from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.order_dtos import DeleteOrderRequest
from order_app.application.repositories import OrderRepository
from order_app.domain.entities.user import UserRole
from order_app.domain.exceptions import OrderNotFoundError


@dataclass
class DeleteOrderUseCase:
    order_repository: OrderRepository

    def execute(self, request: DeleteOrderRequest) -> Result[bool]:
        try:
            order = self.order_repository.get_by_id(request.order_id)
        except OrderNotFoundError:
            return Result.failure(
                Error.not_found(
                    entity="Order", attr_name="id", attr_value=str(request.order_id)
                )
            )

        if request.role != UserRole.MANAGER and order.user_id != request.user_id:
            return Result.failure(
                Error.forbidden(
                    entity="Order", action="delete", entity_id=str(request.order_id)
                )
            )

        self.order_repository.delete(request.order_id)
        return Result.success(True)
