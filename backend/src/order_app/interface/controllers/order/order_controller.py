from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from order_app.application.dtos.order_dtos import (
    DeleteOrderRequest,
    EditOrderRequest,
    ItemRequest,
)
from order_app.application.use_cases.order.create_order import (
    CreateOrderRequest,
    CreateOrderUseCase,
)
from order_app.application.use_cases.order.delete_order import DeleteOrderUseCase
from order_app.application.use_cases.order.edit_order_use_case import EditOrderUseCase
from order_app.application.use_cases.order.list_order_use_case import (
    ListOrderRequest,
    ListOrderUseCase,
)
from order_app.domain.value_objects.user_role import UserRole
from order_app.interface.common.operation_result import OperationResult
from order_app.interface.presenters.base import OrderPresenter
from order_app.interface.view_models.order_vm import OrderViewModel


# COMMON DTOS
@dataclass
class AuthContext:
    user_id: str
    role: Literal["manager", "customer"]


# CREATE ORDER DTOS
@dataclass
class ItemRequestData:
    product_id: str
    quantity: int


@dataclass
class CreateOrderRequestData:
    auth: AuthContext
    items: list[ItemRequestData]


@dataclass
class CreateOrderResponseData:
    order_id: str


@dataclass
class EditProductInOrderRequestData:
    auth: AuthContext
    order_id: str
    product_id: str
    quantity: int


@dataclass
class ListOderRequestData:
    auth: AuthContext


@dataclass
class DeleteOrderRequestData:
    auth: AuthContext
    order_id: str


@dataclass
class OrderController:
    create_order_use_case: CreateOrderUseCase
    list_order_user_case: ListOrderUseCase
    edit_order_use_case: EditOrderUseCase
    delete_order_use_case: DeleteOrderUseCase
    presenter: OrderPresenter

    def handle_create(
        self, request_data: CreateOrderRequestData
    ) -> OperationResult[OrderViewModel]:
        request = CreateOrderRequest(
            user_id=UUID(request_data.auth.user_id),
            items=[
                ItemRequest(product_id=item.product_id, quantity=item.quantity)
                for item in request_data.items
            ],
        )
        response = self.create_order_use_case.execute(request)
        if response.is_success:
            view_model = self.presenter.present_order(response.value)
            return OperationResult.succeed(view_model)
        else:
            error_vm = self.presenter.present_error(
                response.error.message, response.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_remove(self, request_data: DeleteOrderRequestData):
        user_id = UUID(request_data.auth.user_id)
        response = self.delete_order_use_case.execute(
            DeleteOrderRequest(
                order_id=request_data.order_id,
                user_id=user_id,
                role=UserRole.from_str(request_data.auth.role),
            )
        )
        if response:
            view_model = self.presenter.present_remove(response.value)
            return OperationResult.succeed(view_model)
        else:
            error_vm = self.presenter.present_error(
                response.error.message, response.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_edit(
        self, request_data: EditProductInOrderRequestData
    ) -> OperationResult[OrderViewModel]:
        request = EditOrderRequest(
            order_id=request_data.order_id,
            user_id=request_data.auth.user_id,
            role=UserRole.from_str(request_data.auth.role),
            product_id=request_data.product_id,
            quantity=request_data.quantity,
        )
        response = self.edit_order_use_case.execute(request)
        if response.is_success:
            view_model = self.presenter.present_order(response.value)
            return OperationResult.succeed(view_model)
        else:
            error_vm = self.presenter.present_error(
                response.error.message, response.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)

    def handle_list(
        self, request_data: ListOderRequestData
    ) -> OperationResult[OrderViewModel]:
        user_id = UUID(request_data.auth.user_id)
        response = self.list_order_user_case.execute(
            ListOrderRequest(user_id, UserRole.from_str(request_data.auth.role))
        )
        if response:
            view_model = self.presenter.present_order_list(response.value)
            return OperationResult.succeed(view_model)
        else:
            error_vm = self.presenter.present_error(
                response.error.message, response.error.code
            )
            return OperationResult.fail(error_vm.message, error_vm.code)
