# accounts/api/urls.py

from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views
# from knox.views import LogoutView, LogoutAllView
# from .views import UserAPIView, RegisterAPIView, LoginAPIView

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    # url(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]