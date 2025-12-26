from decimal import Decimal
from uuid import uuid4

import pytest

from order_app.domain.entities.order import Order, OrderItem, OrderStatus
from order_app.domain.entities.product import Product
from order_app.domain.value_objects.money import Money


@pytest.fixture
def order(user_customer):
    return Order.new(user_id=user_customer.id)


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
        product_id=product.id, quantity=2, unit_price=product.price
    )


def test_load_items(order):
    product_1 = Product(
        id=uuid4(),
        name="Test Product 1",
        description="A test product 1",
        price=Money(Decimal("10.00")),
        stock_quantity=10,
    )
    product_2 = Product(
        id=uuid4(),
        name="Test Product 2",
        description="A test product 2",
        price=Money(Decimal("5.00")),
        stock_quantity=5,
    )
    order.load_items(items=[(product_1, 10), (product_2, 5)])
    assert order.item_count == 2
    assert order.get_items() == [
        OrderItem(product_id=product_1.id, quantity=10, unit_price=product_1.price),
        OrderItem(product_id=product_2.id, quantity=5, unit_price=product_2.price),
    ]


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


def test_edit_order_item_increase(order):
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

    order.edit_item(product1, 3)

    assert order.items[0].quantity == 3
    assert order.items[1].quantity == 5


def test_edit_order_item_decrease(order):
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

    order.edit_item(product1, 1)

    assert order.items[0].quantity == 1
    assert order.items[1].quantity == 5
