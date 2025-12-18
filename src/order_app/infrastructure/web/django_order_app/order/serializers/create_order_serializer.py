from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderRequestSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField())
