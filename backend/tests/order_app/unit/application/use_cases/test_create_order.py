from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from freezegun import freeze_time

from order_app.application.dtos.order_dtos import ItemRequest
from order_app.application.use_cases.order.create_order import (
    CreateOrderRequest,
    CreateOrderUseCase,
)
from order_app.domain.entities.order import Order
from order_app.domain.exceptions import InsufficientStockError, ProductNotFoundError
from order_app.domain.value_objects.money import Money


def test_create_order_product_not_found(order_repository, product_repository):
    use_case = CreateOrderUseCase(
        order_repository=order_repository,
        product_repository=product_repository,
    )

    user_id = uuid4()
    product_id = uuid4()
    request = CreateOrderRequest(
        user_id=user_id,
        items=[ItemRequest(product_id=product_id, quantity=1)],
    )

    product_repository.get_by_id.side_effect = ProductNotFoundError(product_id)

    result = use_case.execute(request)

    product_repository.get_by_id.assert_called_once_with(product_id)
    assert not result.is_success


def test_create_order_insufficient_stock(order_repository, product_repository):
    use_case = CreateOrderUseCase(
        order_repository=order_repository,
        product_repository=product_repository,
    )

    user_id = uuid4()
    product_id = uuid4()
    product = MagicMock(
        id=product_id, price=Money(Decimal("100.00")), stock_quantity=100
    )
    product.decrease_stock.side_effect = InsufficientStockError(product_id)
    request = CreateOrderRequest(
        user_id=user_id,
        items=[ItemRequest(product_id=product_id, quantity=101)],
    )

    product_repository.get_by_id.return_value = product

    result = use_case.execute(request)

    product_repository.get_by_id.assert_called_once_with(product_id)
    assert not result.is_success


@freeze_time("2022-01-01")
def test_create_order(order_repository, product_repository):
    use_case = CreateOrderUseCase(
        order_repository=order_repository,
        product_repository=product_repository,
    )
    user_id = uuid4()
    product_id_1 = uuid4()
    product_id_2 = uuid4()
    product_1 = MagicMock(
        id=product_id_1, price=Money(Decimal("100.00")), stock_quantity=100
    )
    product_2 = MagicMock(
        id=product_id_2, price=Money(Decimal("50.00")), stock_quantity=50
    )
    product_repository.get_by_id.side_effect = [product_1, product_2]

    request = CreateOrderRequest(
        user_id=user_id,
        items=[
            ItemRequest(product_id=product_id_1, quantity=2),
            ItemRequest(product_id=product_id_2, quantity=1),
        ],
    )
    result = use_case.execute(request)

    product_repository.create.assert_any_call(product_1)
    product_repository.create.assert_any_call(product_2)
    desired_order = Order.new(user_id=user_id)
    desired_order.id = result.value.order_id
    desired_order.add_item(product_1, quantity=2)
    desired_order.add_item(product_2, quantity=1)
    order_repository.create.assert_called_once_with(desired_order)

    assert result.value.user_id == request.user_id
    assert result.value.item_count == 2
    assert result.value.items == [
        {
            "product_id": product_id_1,
            "quantity": 2,
            "unit_price": str(Money(Decimal("100"))),
        },
        {
            "product_id": product_id_2,
            "quantity": 1,
            "unit_price": str(Money(Decimal("50"))),
        },
    ]
