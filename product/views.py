from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Product
from . import serializers
from product.permissions import IsAuthor


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
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]
