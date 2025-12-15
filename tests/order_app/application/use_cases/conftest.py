from unittest.mock import MagicMock

import pytest


@pytest.fixture
def order_repository():
    class MockOrderRepository:
        def __init__(self):
            self.save = MagicMock()
            self.delete = MagicMock()
            self.get_by_id = MagicMock()
            self.get_list = MagicMock()

    return MockOrderRepository()


@pytest.fixture
def product_repository():
    class MockProductRepository:
        def __init__(self):
            self.get_by_id = MagicMock()
            self.update = MagicMock()

    return MockProductRepository()
