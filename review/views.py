from rest_framework import generics, permissions, mixins
from .models import Review
from rest_framework.generics import GenericAPIView
from . import serializers
from .permissions import IsAuthorOrAdminOrPostOwner
from product.permissions import IsAuthor


class CustomUpdateDestroy(mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewDetailView(CustomUpdateDestroy):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewCreateSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAuthorOrAdminOrPostOwner()]
        return [permissions.IsAuthenticatedOrReadOnly()]

