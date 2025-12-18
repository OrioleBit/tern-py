from dataclasses import dataclass

from order_app.application.common.result import Result
from order_app.application.dtos.order_dtos import ListOrderRequest, OrderResponse
from order_app.application.repositories import OrderRepository
from order_app.domain.entities.user import UserRole


@dataclass
class ListOrderUseCase:
    order_repository: OrderRepository

    def execute(self, request: ListOrderRequest) -> Result[list[OrderResponse]]:
        if request.role != UserRole.MANAGER:
            order_list = self.order_repository.get_list(request.user_id)
        else:
            order_list = self.order_repository.get_list()

        return Result.success(
            [OrderResponse.from_entity(order) for order in order_list]
        )
