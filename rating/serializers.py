from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    product = serializers.ReadOnlyField(source='product.id')

    class Meta:
        model = Rating
        fields = '__all__'

