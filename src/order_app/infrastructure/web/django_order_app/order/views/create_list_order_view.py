from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order_app.infrastructure.web.django_order_app.django_order_app.composition_root import (
    composition_root,
)
from order_app.infrastructure.web.django_order_app.user.models import User
from order_app.interface.controllers.order_controller import (
    AuthContext,
    CreateOrderRequestData,
    ItemRequestData,
    ListOderRequestData,
)

from ..serializers import CreateOrderRequestSerializer


class CreateListOrderView(generics.CreateAPIView, generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        operation_result = composition_root.order_controller.handle_create(
            CreateOrderRequestData(
                auth=AuthContext(
                    user_id=str(request.user.id), role=request.user.groups.first().name
                ),
                items=[
                    ItemRequestData(
                        product_id=item["product_id"], quantity=item["quantity"]
                    )
                    for item in serializer.validated_data["items"]
                ],
            )
        )
        if operation_result.is_success:
            return Response(data={"order_id": operation_result.success.id})
        else:
            return Response(
                data={"error": operation_result.error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, *args, **kwargs):
        user: User = request.user
        operation_result = composition_root.order_controller.handle_list(
            ListOderRequestData(
                auth=AuthContext(
                    user_id=str(request.user.id), role=user.groups.first().name
                )
            )
        )
        if operation_result.is_success:
            return Response(
                data=[
                    {
                        "order_id": order.id,
                        "user_id": order.user_id,
                        "items": [
                            {
                                "product_id": item["product_id"],
                                "quantity": item["quantity"],
                            }
                            for item in order.items
                        ],
                        "created_at": order.created_at,
                        "updated_at": order.updated_at,
                    }
                    for order in operation_result.success
                ]
            )
        else:
            return Response(
                data={"error": operation_result.error.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
