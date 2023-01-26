from django.shortcuts import render
from .serializers import RatingSerializer
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Rating


# Create your views here.
# class AddStarRatingView(APIView):
#
#     def post(self, request):
#         serializer = RatingSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user.id)
#             return Response(request.data, status=201)
#         else:
#             return Response(status=400)


class AddStarRatingView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        # print(serializer, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
        serializer.save(user=self.request.user)
