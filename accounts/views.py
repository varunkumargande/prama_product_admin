from django.shortcuts import render

# Create your views here.
from django.contrib.auth.signals import user_logged_in

from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from knox.models import AuthToken
from knox.settings import knox_settings

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
          "user": UserSerializer(user, context=self.get_serializer_context()).data,
          "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        # _, will make value to JSON serializable
        _, token = AuthToken.objects.create(user, token_ttl)
        user_logged_in.send(sender=user.__class__,request=request, user=user)
        return Response({
          "user": UserSerializer(user, context=self.get_serializer_context()).data,
          "token": token
        })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
