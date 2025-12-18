from uuid import UUID

from order_app.application.repositories import ProductRepository
from order_app.domain.entities.product import Product
from order_app.domain.value_objects.money import Money

from ..models import Product as DjangoProduct


class DjangoProductRepository(ProductRepository):
    def save(self, product: Product) -> None:
        DjangoProduct.objects.update_or_create(
            id=product.id,
            defaults={
                "name": product.name,
                "description": product.description,
                "price": product.price.amount,
                "stock_quantity": product.stock_quantity,
            },
        )

    def get_by_id(self, product_id: UUID) -> Product:
        django_product = DjangoProduct.objects.get(id=product_id)
        return Product.from_existing(
            id=django_product.id,
            name=django_product.name,
            description=django_product.description,
            price=Money(django_product.price),
            stock_quantity=django_product.stock_quantity,
            created_at=django_product.created_at,
            updated_at=django_product.updated_at,
        )
