from rest_framework import serializers
from .models import Order, OrderItem
from .tasks import send_confirmation_email


user_id = serializers.ReadOnlyField(source='user.id')


class OrderCreateSerializer(serializers.ModelSerializer):
    user = user_id
    user_email = serializers.ReadOnlyField(source='user.email')
    final_price = serializers.ReadOnlyField()
    activation_code = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        import uuid
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        final_price = sum([price['final_price'] for price in order.products.values()])
        order.final_price = final_price
        order.activation_code = str(uuid.uuid4())
        order.save()

        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        instance.products.set(products)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        final_price = sum([price['final_price'] for price in instance.products.values()])
        # print(instance.products.values(), '!!!!!!!!!')
        instance.final_price = final_price
        instance.save()
        return instance


        # print(dir(order))
        # order = Order.objects.create(final_price=final_price)
        # print(order)
        # print(order.products.values(), '!!!!!!!!!!!')
        # for price in order.products.values():
        #     print(price['final_price'])


class OrderListSerializer(serializers.ModelSerializer):
    user = user_id

    class Meta:
        model = Order
        exclude = ('activation_code',)


class OrderItemSerializer(serializers.ModelSerializer):
    user = user_id
    final_price = serializers.ReadOnlyField()
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = '__all__'





