from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Order, OrderItem
from rest_framework.views import APIView
from . import serializers
from .permissions import IsAuthor
from .tasks import send_confirmation_email

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
        user = serializer.save(user=self.request.user)
        email = serializer.data['email']
        if email:
            send_confirmation_email(email, user.activation_code)
        send_confirmation_email.delay(str(user.user), user.activation_code)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            logger.warning('only author')
            return [permissions.IsAuthenticated(), IsAuthor()]
        logger.warning('only authenticated user')
        return [permissions.IsAuthenticated()]


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            order = Order.objects.get(activation_code=activation_code)
            order.is_active = True
            order.activation_code = ''
            order.save()
            return Response({'msg': 'Successfully confirmed!'}, status=200)
        except Exception:
            return Response({'msg': 'Link expired!'}, status=400)


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def perform_create(self, serializer):
        logger.info('save')
        serializer.save(user=self.request.user)



