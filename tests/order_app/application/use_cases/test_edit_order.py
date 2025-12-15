from unittest import mock
from uuid import uuid4

import pytest

from order_app.application.use_cases.edit_order_use_case import (
    EditOrderRequest,
    EditOrderUseCase,
)
from order_app.domain.entities.user import UserRole


def test_edit_order_not_found_raises(order_repository, product_repository):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )
    order_repository.get_by_id.return_value = None

    order_id = uuid4()
    user_id = uuid4()
    product_id = uuid4()
    request = EditOrderRequest(
        order_id=order_id,
        user_id=user_id,
        role=UserRole.CUSTOMER,
        product_id=product_id,
        quantity=10,
    )

    with pytest.raises(ValueError, match=f"Order with ID {order_id} not found"):
        edit_order_use_case.execute(request)


def test_edit_product_not_found_raises(order_repository, product_repository):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )

    order_id = uuid4()
    user_id = uuid4()
    product_id = uuid4()

    mock_order = mock.Mock()
    mock_order.user_id = user_id
    mock_order.order_id = order_id
    order_repository.get_by_id.return_value = mock_order

    product_repository.get_by_id.return_value = None

    request = EditOrderRequest(
        order_id=order_id,
        user_id=user_id,
        role=UserRole.CUSTOMER,
        product_id=product_id,
        quantity=10,
    )

    with pytest.raises(ValueError, match=f"Product with ID {product_id} not found"):
        edit_order_use_case.execute(request)


def test_edit_product_without_permission_by_customer_raises(
    order_repository, product_repository
):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )

    order_id = uuid4()
    user_id = uuid4()
    other_user_id = uuid4()
    product_id = uuid4()

    mock_order = mock.Mock()
    mock_order.user_id = user_id
    mock_order.order_id = order_id
    order_repository.get_by_id.return_value = mock_order

    mock_product = mock.Mock()
    mock_product.product_id = product_id
    product_repository.get_by_id.return_value = mock_product

    request = EditOrderRequest(
        order_id=order_id,
        user_id=other_user_id,
        role=UserRole.CUSTOMER,
        product_id=product_id,
        quantity=10,
    )

    with pytest.raises(
        ValueError, match="You don't have permission to edit this order"
    ):
        edit_order_use_case.execute(request)


def test_edit_product_with_permission_by_customer(order_repository, product_repository):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )

    order_id = uuid4()
    user_id = uuid4()
    product_id = uuid4()

    mock_order = mock.Mock()
    mock_order.user_id = user_id
    mock_order.order_id = order_id
    order_repository.get_by_id.return_value = mock_order

    mock_product = mock.Mock()
    mock_product.product_id = product_id
    product_repository.get_by_id.return_value = mock_product

    request = EditOrderRequest(
        order_id=order_id,
        user_id=user_id,
        role=UserRole.CUSTOMER,
        product_id=product_id,
        quantity=10,
    )

    edit_order_use_case.execute(request)

    mock_order.edit_item.assert_called_once_with(product_id, 10)
    order_repository.save.assert_called_once_with(mock_order)
