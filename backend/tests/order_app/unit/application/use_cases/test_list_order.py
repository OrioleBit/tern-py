from uuid import uuid4

from order_app.application.use_cases.order.list_order_use_case import (
    ListOrderRequest,
    ListOrderUseCase,
)
from order_app.domain.entities.user import UserRole


def test_list_order_use_case_user_manager(order_repository):
    user_id = uuid4()
    use_case = ListOrderUseCase(order_repository=order_repository)
    request = ListOrderRequest(user_id=user_id, role=UserRole.MANAGER)

    use_case.execute(request)

    order_repository.get_list.assert_called_once_with()


def test_list_order_use_case_user_customer(order_repository):
    user_id = uuid4()
    use_case = ListOrderUseCase(order_repository=order_repository)
    request = ListOrderRequest(user_id=user_id, role=UserRole.CUSTOMER)

    use_case.execute(request)

    order_repository.get_list.assert_called_once_with(user_id)
