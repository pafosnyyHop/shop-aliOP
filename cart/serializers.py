from rest_framework import serializers
from .models import Order, OrderItem


user_id = serializers.ReadOnlyField(source='user.id')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = user_id
    user_email = serializers.ReadOnlyField(source='user.email')
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        final_price = sum([price['final_price'] for price in order.products.values()])
        order.final_price = final_price

        # print(dir(order))
        # order = Order.objects.create(final_price=final_price)
        # print(order)
        # print(order.products.values(), '!!!!!!!!!!!')
        # for price in order.products.values():
        #     print(price['final_price'])

        return order


class OrderListSerializer(serializers.ModelSerializer):
    user = user_id

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    user = user_id
    final_price = serializers.ReadOnlyField()
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = '__all__'





