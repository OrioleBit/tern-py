from order_app.application.dtos.order_dtos import OrderResponse
from order_app.interface.presenters.base import OrderPresenter
from order_app.interface.view_models.error_vm import ErrorViewModel
from order_app.interface.view_models.order_vm import OrderViewModel


class WebOrderPresenter(OrderPresenter):
    def present_order(order_response: OrderResponse) -> OrderViewModel:
        return OrderViewModel(
            id=str(order_response.order_id),
            user_id=str(order_response.user_id),
            items=order_response.items,
            created_at=order_response.created_at,
            updated_at=order_response.updated_at,
            total_price=order_response.total_price,
        )

    def present_order_list(
        order_list_response: list[OrderResponse],
    ) -> list[OrderViewModel]:
        return [WebOrderPresenter.present_order(order) for order in order_list_response]

    def present_error(error, code=None) -> ErrorViewModel:
        return ErrorViewModel(error, str(code))
