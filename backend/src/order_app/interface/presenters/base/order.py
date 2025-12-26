from abc import ABC, abstractmethod

from order_app.application.dtos.order_dtos import OrderResponse
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.order_vm import OrderViewModel


class OrderPresenter(ABC):
    @abstractmethod
    def present_order(order_response: OrderResponse) -> OrderViewModel:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def present_order_list(
        order_list_response: list[OrderResponse],
    ) -> list[OrderViewModel]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def present_remove(result: bool) -> list[OrderViewModel]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def present_error(error: str, code: str | None = None) -> ErrorViewModel:
        raise NotImplementedError  # pragma: no cover
