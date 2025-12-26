from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from freezegun import freeze_time

from order_app.application.common.result import Error, Result
from order_app.application.dtos.order_dtos import CreateOrderRequest, ItemRequest
from order_app.interface.controllers.order.order_controller import (
    AuthContext,
    CreateOrderRequestData,
    ItemRequestData,
    OrderController,
)
from order_app.interface.presenters.base import OrderPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel


@pytest.fixture
def create_order_use_case(order_repository, product_repository):
    class MockCreateOrderUseCase:
        def __init__(self):
            self.execute = MagicMock()
            self.order_repository = order_repository
            self.product_repository = product_repository

    return MockCreateOrderUseCase()


@pytest.fixture
def list_order_use_case(order_repository):
    class MockCreateOrderUseCase:
        def __init__(self):
            self.execute = MagicMock()
            self.order_repository = order_repository

    return MockCreateOrderUseCase()


def test_create_order_handler_failure(create_order_use_case):
    create_order_use_case.execute.return_value = Result.failure(Error("error", "code"))
    mock_presenter = MagicMock(spec=OrderPresenter)
    mock_presenter.present_error.return_value = ErrorViewModel("errordata", "codedata")

    order_controller = OrderController(
        create_order_use_case=create_order_use_case,
        list_order_user_case=None,
        edit_order_use_case=None,
        delete_order_use_case=None,
        presenter=mock_presenter,
    )
    user_id = uuid4()
    product_id_1 = uuid4()
    product_id_2 = uuid4()
    request_data = CreateOrderRequestData(
        auth=AuthContext(user_id=str(user_id), role="customer"),
        items=[
            ItemRequestData(product_id=product_id_1, quantity=1),
            ItemRequestData(product_id=product_id_2, quantity=2),
        ],
    )

    operation_result = order_controller.handle_create(request_data=request_data)

    create_order_use_case.execute.assert_called_once_with(
        CreateOrderRequest(
            user_id=user_id,
            items=[
                ItemRequest(product_id=item.product_id, quantity=item.quantity)
                for item in request_data.items
            ],
        )
    )
    mock_presenter.present_error.assert_called_once_with("code", "error")
    assert not operation_result.is_success
    assert operation_result.error.code == "codedata"
    assert operation_result.error.message == "errordata"


@freeze_time("2022-01-01")
def test_create_order_handler_success(create_order_use_case):
    product_id_1 = uuid4()
    product_id_2 = uuid4()
    user_id = uuid4()

    use_case_response = Result.success(value="A_Use_Case_Response")
    create_order_use_case.execute.return_value = use_case_response
    mock_presenter = MagicMock()
    mock_presenter.present_order.return_value = "A_View_Model"

    order_controller = OrderController(
        create_order_use_case=create_order_use_case,
        list_order_user_case=None,
        edit_order_use_case=None,
        delete_order_use_case=None,
        presenter=mock_presenter,
    )

    request_data = CreateOrderRequestData(
        auth=AuthContext(user_id=str(user_id), role="customer"),
        items=[
            ItemRequest(product_id=product_id_1, quantity=1),
            ItemRequest(product_id=product_id_2, quantity=2),
        ],
    )

    operation_result = order_controller.handle_create(request_data=request_data)

    create_order_use_case.execute.assert_called_once_with(
        CreateOrderRequest(user_id=user_id, items=request_data.items)
    )
    mock_presenter.present_order.assert_called_once_with("A_Use_Case_Response")
    assert operation_result.is_success
