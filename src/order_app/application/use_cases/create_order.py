from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.order_dtos import CreateOrderRequest, OrderResponse
from order_app.application.exception import ProductNotFoundError
from order_app.application.repositories import OrderRepository, ProductRepository
from order_app.domain.entities.order import Order


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepository
    product_repository: ProductRepository

    def execute(self, request: CreateOrderRequest) -> Result[OrderResponse]:
        order = Order.new(user_id=request.user_id)
        products = []
        for item in request.items:
            product_id = item.product_id
            try:
                product = self.product_repository.get_by_id(product_id)
            except ProductNotFoundError:
                return Result.failure(Error.not_found("Product", str(product_id)))
            order.add_item(product, item.quantity)
            products.append(product)

        for product in products:
            print(product)
            self.product_repository.save(product)
        self.order_repository.save(order)
        return Result.success(OrderResponse.from_entity(order))
