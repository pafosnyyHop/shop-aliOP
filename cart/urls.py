from django.urls import path
from . import views


urlpatterns = [
    path('order/<uuid:activation_code>/', views.ActivationView.as_view())
]
