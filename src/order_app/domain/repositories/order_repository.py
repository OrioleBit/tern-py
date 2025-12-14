from abc import ABC, abstractmethod
from order_app.domain.entities.order import Order
from uuid import UUID


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order to the repository."""
        pass

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order:
        """Retrieve an order by its ID."""
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> list[Order]:
        """Retrieve all orders for a specific user."""
        pass
