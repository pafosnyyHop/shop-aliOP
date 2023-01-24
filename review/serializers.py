from rest_framework import serializers
from review.models import Review, ReviewImages


class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImages
        fields = '__all__'


class ReviewCreateSerializer(serializers.ModelSerializer):
    images = ReviewImageSerializer(many=True, read_only=False, required=False)
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        review = Review.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            ReviewImages.objects.create(image=image, review=review)
        return review

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['images'] = ReviewImageSerializer(instance.images.all(), many=True).data

        return repr
