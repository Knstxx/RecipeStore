from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet


recipe_router = DefaultRouter()
recipe_router.register(r'recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(recipe_router.urls)),
]
