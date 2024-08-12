from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CustomUserViewSet

user_router = DefaultRouter()
user_router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/',
         include('djoser.urls.authtoken')
         ),
    path('', include(user_router.urls)),
]
