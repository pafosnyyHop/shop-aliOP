from rest_framework import serializers
from category.models import Category
from .models import Product, ProductImages
from review.serializers import ReviewCreateSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    images = ProductImageSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        product = Product.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            ProductImages.objects.create(image=image, product=product)
        return product

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['images'] = ProductImageSerializer(instance.images.all(), many=True).data
        repr['reviews'] = ReviewCreateSerializer(instance.reviews.all(), many=True).data

        return repr


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'title', 'price', 'preview', 'owner_email')








