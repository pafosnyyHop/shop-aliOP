from django.shortcuts import render
from .serializers import RatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rating

import logging

logger = logging.getLogger('main')


# Create your views here.
class AddStarRatingView(APIView):

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user.id)
            logger.info('added stars')
            return Response(request.data, status=201)
        else:
            logger.error('error')
            return Response(status=400)



