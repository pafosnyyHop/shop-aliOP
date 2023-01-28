from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from favorites.models import Favorites
from .models import Product
from likes.models import Like
from . import serializers
from product.permissions import IsAuthor
from rating.models import Rating, RatingStar

import logging


class StandartResultPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 1000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('?')
    pagination_class = StandartResultPagination
    django_filters = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'stock', 'price', 'owner')
    search_fields = ('title', 'email', 'username')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            logger.info('list')
            return serializers.ProductListSerializer
        logger.info('product added')
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            logger.warning('only authenticated, author, admin user ')
            return [permissions.IsAuthenticated(), IsAuthor(), permissions.IsAdminUser()]
        logger.info('done')
        return [permissions.IsAuthenticated()]

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method in ('POST', 'UPDATE'):
            if user.favorites.filter(product=product).exists():
                logger.error('product already in favorites')
                return Response('This product is already in favorites!',
                                status=400)
            Favorites.objects.create(owner=user, product=product)
            logger.info('added to favorites')
            return Response('Added to favorites!', status=201)
        else:
            if user.favorites.filter(product=product).exists():
                user.favorites.filter(product=product).delete()
                logger.info('success delete')
                return Response('Deleted from favorites!', status=204)
            logger.error('not found')
            return Response('Product is not found!', status=400)

    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_posts.filter(product=product).exists():
                return Response('This product is already liked!', status=400)
            Like.objects.create(owner=user, product=product)
            return Response('You liked the product!', status=201)
        else:
            if not user.liked_posts.filter(product=product).exists():
                return Response('You didn\'t liked this product!', status=400)
            user.liked_posts.filter(product=product).delete()
            return Response('Your like is deleted!', status=204)







