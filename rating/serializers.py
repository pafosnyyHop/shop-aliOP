from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        # print(self, '!!!!!!!!!!!!!!!!!!!!!')
        rating = Rating.objects.update_or_create(
            user=validated_data.get('user', None),
            product=validated_data.get('product', None),
            defaults={'rating': validated_data.get("rating")}
        )
        return rating
