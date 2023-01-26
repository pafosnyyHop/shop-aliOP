from account import views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('password_change/', auth_view.PasswordChangeView.as_view()),
    # path('password_re')
]
