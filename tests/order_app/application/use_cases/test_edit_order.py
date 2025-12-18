from decimal import Decimal
from unittest import mock
from uuid import uuid4

from order_app.application.common.result import Error
from order_app.application.dtos.order_dtos import OrderResponse
from order_app.application.exception import OrderNotFoundError, ProductNotFoundError
from order_app.application.use_cases.edit_order_use_case import (
    EditOrderRequest,
    EditOrderUseCase,
)
from order_app.domain.entities.order import Order
from order_app.domain.entities.product import Product
from order_app.domain.entities.user import UserRole
from order_app.domain.value_objects.money import Money


def test_edit_order_not_found(order_repository, product_repository):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )
    order_repository.get_by_id.side_effect = OrderNotFoundError(uuid4())

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

    result = edit_order_use_case.execute(request)

    order_repository.get_by_id.assert_called_once_with(order_id)
    product_repository.get_by_id.assert_not_called()
    order_repository.save.assert_not_called()
    assert not result.is_success


def test_edit_product_not_found(order_repository, product_repository):
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

    product_repository.get_by_id.side_effect = ProductNotFoundError(product_id)

    request = EditOrderRequest(
        order_id=order_id,
        user_id=user_id,
        role=UserRole.CUSTOMER,
        product_id=product_id,
        quantity=10,
    )

    result = edit_order_use_case.execute(request)

    order_repository.get_by_id.assert_called_once_with(order_id)
    product_repository.get_by_id.assert_called_once_with(product_id)
    order_repository.save.assert_not_called()
    assert not result.is_success
    assert result.error == Error.not_found("Product", str(product_id))


def test_edit_product_without_permission_by_customer(
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

    result = edit_order_use_case.execute(request)

    order_repository.get_by_id.assert_called_once_with(order_id)
    product_repository.get_by_id.assert_called_once_with(product_id)
    order_repository.save.assert_not_called()
    assert not result.is_success
    assert result.error == Error.forbidden("Order", str(order_id))


def test_edit_product_with_permission_by_customer(order_repository, product_repository):
    edit_order_use_case = EditOrderUseCase(
        order_repository=order_repository, product_repository=product_repository
    )

    user_id = uuid4()

    order = Order.new(user_id=user_id)
    order.edit_item = mock.Mock()
    product1 = Product.new(
        name="Test Product 1",
        description="A test product 1",
        price=Money(Decimal("10.00")),
        stock_quantity=100,
    )
    product2 = Product.new(
        name="Test Product 2",
        description="A test product 2",
        price=Money(Decimal("5.00")),
        stock_quantity=50,
    )

    order.add_item(product=product1, quantity=10)
    order.add_item(product=product2, quantity=5)
    order_repository.get_by_id.return_value = order

    product_repository.get_by_id.return_value = product1

    request = EditOrderRequest(
        order_id=order.id,
        user_id=user_id,
        role=UserRole.CUSTOMER,
        product_id=product1.id,
        quantity=36,
    )

    result = edit_order_use_case.execute(request)

    order_repository.get_by_id.assert_called_once_with(order.id)
    product_repository.get_by_id.assert_called_once_with(product1.id)
    order.edit_item.assert_called_once_with(product1.id, 36)
    order_repository.save.assert_called_once_with(order)
    assert result.is_success
    assert isinstance(result.value, OrderResponse)
