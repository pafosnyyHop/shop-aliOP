from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from cart.serializers import OrderListSerializer
from favorites.serializers import FavoritePostsSerializer


User = get_user_model()


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20,
                                     required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20,
                                      required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'last_name', 'first_name',
                  'username', 'avatar')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Password did\'t match!')
        if not attrs['password'].isalnum():
            raise serializers.ValidationError('Password field must contain'
                                              'alpha and numeric symbols!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)

    def is_followed(self, req_user, detail_user):
        return req_user.followers.filter(following=detail_user).exists()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['favorite_products'] = FavoritePostsSerializer(instance.favorites.all(), many=True).data
        rep['order'] = OrderListSerializer(instance.userorders.all(), many=True).data
        return rep


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': _('Token is invalid or expired!')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
