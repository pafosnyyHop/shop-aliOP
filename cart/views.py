from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .models import Order, OrderItem
from . import serializers
from .permissions import IsAuthor

import logging


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = permissions.IsAuthenticated()

    def get_serializer_class(self):
        if self.action == 'list':
            logger.info('make order list')
            return serializers.OrderListSerializer
        logger.info('make order')
        return serializers.OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            logger.warning('only author')
            return [permissions.IsAuthenticated(), IsAuthor()]
        logger.warning('only authenticated user')
        return [permissions.IsAuthenticated()]


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def perform_create(self, serializer):
        logger.info('save')
        serializer.save(user=self.request.user)



