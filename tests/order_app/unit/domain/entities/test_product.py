import pytest

from order_app.domain.entities.product import Product
from order_app.domain.exceptions import InsufficientStockError


@pytest.fixture
def product():
    return Product.new(
        name="Test Product",
        description="A product for testing",
        price=10.0,
        stock_quantity=100,
    )


def test_decrease_stock(product):
    initial_stock = product.stock_quantity
    product.decrease_stock(3)
    assert product.stock_quantity == initial_stock - 3


def test_decrease_stock_invalid_quantity(product):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        product.decrease_stock(0)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        product.decrease_stock(-5)


def test_decrease_stock_insufficient(product):
    with pytest.raises(InsufficientStockError, match="Insufficient stock to decrease"):
        product.decrease_stock(product.stock_quantity + 1)


def test_increase_stock_zero_order_negative_quantity(product):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        product.increase_stock(0)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        product.increase_stock(-5)
