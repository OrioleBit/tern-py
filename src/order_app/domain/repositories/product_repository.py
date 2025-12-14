from abc import ABC, abstractmethod
from typing import Optional
from order_app.domain.entities.product import Product
from uuid import UUID


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        """Save a product to the repository."""
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        """Update an existing product in the repository."""
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Retrieve a product by its ID."""
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> list[Product]:
        """Retrieve all products for a specific user."""
        pass
