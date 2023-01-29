from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import views

from . import serializers

from .send_mail import send_confirmation_email
import logging


User = get_user_model()

logger = logging.getLogger('main')


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                try:
                    logger.debug('registration')
                    send_confirmation_email(user.email, user.activation_code)

                except:
                    logger.error('registration problems')
                    return Response({'msg': 'Registered but troubles with mail!',
                                     'data': serializer.data}, status=201)
            logger.error('data problem')
            return Response(serializer.data, status=201)
        logger.warning('bad request')
        return Response('Bad request!', status=400)


class ActivationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            print(user)
            user.is_active = True
            user.activation_code = ''
            user.save()
            logger.warning('activation')
            return Response({'msg': 'Successfully activated!'}, status=200)
        except User.DoesNotExist:
            logger.error('link expired')
            return Response({'msg': 'Link expired!'}, status=400)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info('success logout')
        return Response('Successfully logged out!', status=200)


class UserDetailViews(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permissions_classes = (permissions.IsAuthenticated,)


