from django.urls import path
from . import views


urlpatterns = [
    path('review/', views.ReviewCreateView.as_view()),
    path('review/<int:pk>/', views.ReviewDetailView.as_view())
]