from rest_framework.viewsets import ModelViewSet
from .models import Category
from rest_framework import permissions
from .serializers import CategorySerializer

import logging

logger = logging.getLogger('main')


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            logger.warning('allow any')
            return [permissions.AllowAny()]
        logger.warning('only admin')
        return [permissions.IsAdminUser()]
