from rest_framework import serializers
from .models import Favorites


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.product.title
        preview = instance.product.preview
        repr['product_preview'] = preview.url
        return repr