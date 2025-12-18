from uuid import UUID

from order_app.application.repositories import OrderRepository
from order_app.application.repositories.product_repository import ProductRepository
from order_app.domain.entities.order import Order

from ..models import Order as DjangoOrder
from ..models import OrderItem


class DjangoOrderRepository(OrderRepository):
    def __init__(self, product_repository: ProductRepository):
        super().__init__()
        self.product_repository = product_repository

    def save(self, order: Order) -> None:
        django_order, _ = DjangoOrder.objects.get_or_create(
            id=order.id, user_id=order.user_id
        )
        for item in order.items:
            OrderItem.objects.update_or_create(
                order_id=order.id,
                product_id=item.product_id,
                defaults={
                    "quantity": item.quantity,
                    "price_per_unit": item.price_per_unit.amount,
                },
            )

    def get_by_id(self, order_id: UUID) -> Order:
        django_order = DjangoOrder.objects.get(id=order_id)
        order = self.to_order(django_order)
        return order

    def to_order(self, django_order) -> Order:
        order = Order.from_existing(
            id=django_order.id,
            user_id=django_order.user.id,
            created_at=django_order.created_at,
            updated_at=django_order.updated_at,
        )
        # for item in django_order.items.all():
        order.load_items(
            [
                (
                    self.product_repository.get_by_id(item.product_id),
                    item.quantity,
                )
                for item in django_order.items.all()
            ]
        )
        return order

    def get_list(self, user_id=None) -> list[Order]:
        orders = []
        if user_id:
            orders = DjangoOrder.objects.filter(user_id=user_id)
        else:
            orders = DjangoOrder.objects.all()

        return [self.to_order(order) for order in orders]
