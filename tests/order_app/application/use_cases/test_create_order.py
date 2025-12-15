from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from order_app.application.use_cases.create_order import (
    CreateOrderRequest,
    CreateOrderUseCase,
    ItemRequest,
)
from order_app.domain.entities.order import OrderItem


def test_create_order(order_repository, product_repository):
    use_case = CreateOrderUseCase(
        order_repository=order_repository,
        product_repository=product_repository,
    )
    user_id = uuid4()
    product_id_1 = uuid4()
    product_id_2 = uuid4()
    product_1 = MagicMock(id=product_id_1, price=100)
    product_2 = MagicMock(id=product_id_2, price=50)
    product_repository.get_by_id.side_effect = [product_1, product_2]

    request = CreateOrderRequest(
        user_id=user_id,
        items=[
            ItemRequest(product_id=product_id_1, quantity=2),
            ItemRequest(product_id=product_id_2, quantity=1),
        ],
    )
    order = use_case.execute(request)

    assert order.user_id == request.user_id
    assert order.item_count == 2
    assert order.items == [
        OrderItem(
            product_id=product_id_1,
            quantity=2,
            price_per_unit=100,
        ),
        OrderItem(
            product_id=product_id_2,
            quantity=1,
            price_per_unit=50,
        ),
    ]
    order_repository.save.assert_called_once_with(order)
    product_repository.update.assert_any_call(product_1)
    product_repository.update.assert_any_call(product_2)


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

    product_repository.get_by_id.return_value = None

    with pytest.raises(ValueError):
        use_case.execute(request)
    product_repository.get_by_id.assert_called_once_with(product_id)
