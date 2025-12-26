from dataclasses import dataclass

from order_app.application.common.result import Error, Result
from order_app.application.dtos.order_dtos import CreateOrderRequest, OrderResponse
from order_app.application.repositories import OrderRepository, ProductRepository
from order_app.domain.entities.order import Order
from order_app.domain.exceptions import InsufficientStockError, ProductNotFoundError


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
                return Result.failure(
                    Error.not_found(
                        entity="Product", attr_name="id", attr_value=str(product_id)
                    )
                )
            try:
                order.add_item(product, item.quantity)
            except InsufficientStockError:
                return Result.failure(
                    Error.domain(
                        message=f"Insufficient stock for {product.id} product. Requested {item.quantity}, available {product.stock_quantity}",
                    )
                )
            products.append(product)

        for product in products:
            self.product_repository.create(product)
        self.order_repository.create(order)
        return Result.success(OrderResponse.from_entity(order))
