from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from . import serializers
from .models import Like
from product.permissions import IsAuthor

import logging

logger = logging.getLogger('main')


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        logger.info('save like')
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    logger.warning('only authenticated, author')
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


