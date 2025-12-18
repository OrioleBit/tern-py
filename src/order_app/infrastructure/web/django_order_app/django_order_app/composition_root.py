from order_app.infrastructure.composition_root import CompositionRoot
from order_app.infrastructure.web.django_order_app.order.repositories import (
    DjangoOrderRepository,
)
from order_app.infrastructure.web.django_order_app.product.repositories import (
    DjangoProductRepository,
)
from order_app.interface.presenters.web import WebOrderPresenter

product_repository = DjangoProductRepository()
composition_root = CompositionRoot(
    order_repository=DjangoOrderRepository(product_repository=product_repository),
    product_repository=product_repository,
    order_presenter=WebOrderPresenter,
)
