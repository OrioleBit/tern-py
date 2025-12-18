from decimal import Decimal

import pytest

from order_app.domain.entities.order import Order, OrderItem, OrderStatus
from order_app.domain.entities.product import Product
from order_app.domain.entities.user import User
from order_app.domain.value_objects.money import Money


@pytest.fixture
def order():
    user = User.new(name="Test User", email="test@example.com")
    return Order.new(user_id=user.id)


def test_order_initial_status(order):
    assert order.status == OrderStatus.CREATED
    assert order.item_count == 0
    assert order.total_price == Money(Decimal("0"))


def test_add_order_item(order):
    product = Product.new(
        name="Test Product",
        description="A test product",
        price=Money(Decimal("15.00")),
        stock_quantity=10,
    )
    assert order.item_count == 0
    order.add_item(product=product, quantity=2)
    assert order.item_count == 1
    assert order.total_price == Money(Decimal("30.00"))
    assert order.items[0] == OrderItem(
        product_id=product.id, quantity=2, price_per_unit=product.price
    )


def test_delete_order_item(order):
    product = Product.new(
        name="Test Product",
        description="A test product",
        price=Money(Decimal("15.00")),
        stock_quantity=10,
    )
    order.add_item(product=product, quantity=2)
    assert order.item_count == 1
    order.remove_item(order.items[0])
    assert order.item_count == 0


def test_edit_order_item(order):
    product1 = Product.new(
        name="Test Product1",
        description="A test product1",
        price=Money(Decimal("15.00")),
        stock_quantity=10,
    )

    product2 = Product.new(
        name="Test Product",
        description="A test product",
        price=Money(Decimal("20.00")),
        stock_quantity=25,
    )
    order.add_item(product=product1, quantity=2)
    order.add_item(product=product2, quantity=5)
    assert order.item_count == 2

    order.edit_item(product1.id, 3)

    assert order.items[0].quantity == 3
    assert order.items[1].quantity == 5
