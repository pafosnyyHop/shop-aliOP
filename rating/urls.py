from django.urls import path
from . import views


urlpatterns = [
    path('stars/', views.AddStarRatingView.as_view()),
]