from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .models import Order, OrderItem
from . import serializers
from .permissions import IsAuthor


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = permissions.IsAuthenticated()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.OrderListSerializer
        return serializers.OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticated()]


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



