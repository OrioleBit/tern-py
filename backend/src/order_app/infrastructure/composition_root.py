from dataclasses import dataclass

from order_app.application.ports.password_hasher import PasswordHasher
from order_app.application.repositories import (
    OrderRepository,
    ProductRepository,
    UserRepository,
)
from order_app.application.use_cases.order.create_order import CreateOrderUseCase
from order_app.application.use_cases.order.delete_order import DeleteOrderUseCase
from order_app.application.use_cases.order.edit_order_use_case import EditOrderUseCase
from order_app.application.use_cases.order.list_order_use_case import ListOrderUseCase
from order_app.application.use_cases.user.login import LoginUserUseCase
from order_app.application.use_cases.user.register import RegisterUserUseCase
from order_app.infrastructure.security.argon2_hasher import Argon2PasswordHasher
from order_app.infrastructure.security.pyjwt_service import PyJWTService
from order_app.interface.controllers.order.order_controller import OrderController
from order_app.interface.controllers.user.login_user import LoginUserController
from order_app.interface.controllers.user.register_user import RegisterUserController
from order_app.interface.presenters.base import (
    LoginPresenter,
    OrderPresenter,
    RegisterPresenter,
)


@dataclass
class CompositionRoot:
    order_repository: OrderRepository
    product_repository: ProductRepository
    user_repository: UserRepository
    password_hasher: PasswordHasher
    order_presenter: OrderPresenter
    register_presenter: RegisterPresenter
    login_presenter: LoginPresenter

    def __post_init__(self):
        ##  use cases
        # order use cases
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

        # user use cases
        register_user_use_case = RegisterUserUseCase(
            user_repository=self.user_repository,
            password_hasher=self.password_hasher,
        )
        login_user_use_case = LoginUserUseCase(
            user_repository=self.user_repository,
            password_hasher=self.password_hasher,
            jwt_service=PyJWTService(
                secret_key="your_secret_key_here", expires_in=3600
            ),
        )

        ## controllers
        # order controllers
        self.order_controller = OrderController(
            create_order_use_case=create_order_use_case,
            list_order_user_case=list_order_use_case,
            edit_order_use_case=edit_order_use_case,
            delete_order_use_case=delete_order_use_case,
            presenter=self.order_presenter,
        )

        # user controllers
        self.register_controller = RegisterUserController(
            register_user_use_case=register_user_use_case,
            presenter=self.register_presenter,
        )
        self.login_controller = LoginUserController(
            login_user_use_case=login_user_use_case,
            presenter=self.login_presenter,
        )
