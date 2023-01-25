from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        product = attrs['Product']
        if user.liked_posts.filter(Product=Product).exists():
            raise serializers.ValidationError('You already liked this post!')
        return attrs


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'Product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.post.title
        preview = instance.post.preview
        repr['product_preview'] = preview.url
        return repr
