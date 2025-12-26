from abc import ABC, abstractmethod
from uuid import UUID

from order_app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> None:
        """Save a product to the repository."""
        raise NotImplementedError  # pragma: no cover

    def update(self, product: Product) -> None:
        """Update a product in the repository."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Product | None:
        """
        Retrieve a product by its ID.

        Raises:
            ProductNotFoundError: If no product exists with the given ID
        """
        raise NotImplementedError  # pragma: no cover
