from order_app.domain.entities.order import Order, OrderItem, OrderStatus
from decimal import Decimal
import pytest
from uuid import uuid4

from order_app.domain.entities.product import Product


@pytest.fixture
def order():
    return Order(
        user_id=uuid4(),
    )


def test_order_initial_status(order):
    assert order.status == OrderStatus.CREATED
    assert order.item_count == 0
    assert order.total_price == Decimal("0")


def test_add_order_item(order):
    product = Product(
        name="Test Product",
        description="A test product",
        price=Decimal("15.00"),
        stock_quantity=10,
    )
    assert order.item_count == 0
    order.add_item(product=product, quantity=2)
    assert order.item_count == 1
    assert order.total_price == Decimal("30.00")
    assert order.items[0] == OrderItem(
        product_id=product.id, quantity=2, price_per_unit=product.price
    )
