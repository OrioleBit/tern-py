from abc import ABC, abstractmethod
from uuid import UUID

from order_app.domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> None:
        """Save an order to the repository."""
        raise NotImplementedError  # pragma: no cover

    def update(self, order: Order) -> None:
        """Update an order in the repository."""
        raise NotImplementedError  # pragma: no cover

    def delete(self, order_id: UUID) -> None:
        """Delete an order from the repository."""
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order:
        """
        Retrieve an order by its ID.

        Raises:
            OrderNotFoundError: If no order exists with the given ID
        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_list(self, user_id: UUID | None = None) -> list[Order]:
        """Retrieve list of orders optionally filtered by specific user ID."""
        raise NotImplementedError  # pragma: no cover
