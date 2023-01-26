from rest_framework import serializers
from .models import Like
from .models import Product


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['product']
        if user.liked_products.filter(product=product).exists():
            raise serializers.ValidationError('You already liked this product!')
        return attrs


class LikedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.product.title
        preview = instance.product.preview
        repr['product_preview'] = preview.url
        return repr
