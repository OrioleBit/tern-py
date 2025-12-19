from dataclasses import dataclass

from order_app.application.repositories import OrderRepository, ProductRepository
from order_app.application.use_cases.create_order import CreateOrderUseCase
from order_app.application.use_cases.delete_order import DeleteOrderUseCase
from order_app.application.use_cases.edit_order_use_case import EditOrderUseCase
from order_app.application.use_cases.list_order_use_case import ListOrderUseCase
from order_app.interface.controllers.order_controller import OrderController
from order_app.interface.presenters.base import OrderPresenter


@dataclass
class CompositionRoot:
    order_repository: OrderRepository
    product_repository: ProductRepository
    order_presenter: OrderPresenter

    def __post_init__(self):
        create_order_use_case = CreateOrderUseCase(
            order_repository=self.order_repository,
            product_repository=self.product_repository,
        )
        list_order_use_case = ListOrderUseCase(order_repository=self.order_repository)
        edit_order_use_case = EditOrderUseCase(
            order_repository=self.order_repository,
            product_repository=self.product_repository,
        )
        delete_order_use_case = DeleteOrderUseCase(
            order_repository=self.order_repository
        )

        self.order_controller = OrderController(
            create_order_use_case=create_order_use_case,
            list_order_user_case=list_order_use_case,
            edit_order_use_case=edit_order_use_case,
            delete_order_use_case=delete_order_use_case,
            presenter=self.order_presenter,
        )
