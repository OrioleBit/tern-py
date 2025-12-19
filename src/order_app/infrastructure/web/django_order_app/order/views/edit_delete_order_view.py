from uuid import UUID

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order_app.application.dtos.order_dtos import EditOrderRequest
from order_app.infrastructure.web.django_order_app.django_order_app.composition_root import (
    composition_root,
)
from order_app.infrastructure.web.django_order_app.order.models import Order
from order_app.infrastructure.web.django_order_app.order.repositories.order_repository import (
    DjangoOrderRepository,
)
from order_app.infrastructure.web.django_order_app.order.serializers import (
    EditOrderRequestSerializer,
)
from order_app.interface.controllers.order_controller import (
    AuthContext,
    DeleteOrderRequestData,
    EditProductInOrderRequestData,
)


class EditOrderView(generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EditOrderRequestSerializer
    http_method_names = ["patch", "delete"]

    def update(self, request, order_id: str, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_result = composition_root.order_controller.handle_edit(
            EditProductInOrderRequestData(
                auth=AuthContext(
                    user_id=self.request.user.id,
                    role=self.request.user.groups.first().name,
                ),
                order_id=order_id,
                product_id=serializer.validated_data["item"]["product_id"],
                quantity=serializer.validated_data["item"]["quantity"],
            )
        )
        if operation_result.is_success:
            return Response(data={"order_id": operation_result.success.id})
        else:
            return Response(
                data={
                    "error": operation_result.error.message,
                    "code": operation_result.error.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, order_id: str, *args, **kwargs):
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                data={"error": "Order not found", "code": "order_not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        operation_result = composition_root.order_controller.handle_remove(
            DeleteOrderRequestData(
                auth=AuthContext(
                    user_id=str(self.request.user.id),
                    role=self.request.user.groups.first().name,
                ),
                order_id=order_id,
            )
        )
        if operation_result.is_success:
            return Response()
        else:
            return Response(
                data={
                    "error": operation_result.error.message,
                    "code": operation_result.error.code,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
