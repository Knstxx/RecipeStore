from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (TagViewSet, IngredientViewSet,
                       CustomUserViewSet, RecipeViewSet)


tags_router = DefaultRouter()
ingredients_router = DefaultRouter()
user_router = DefaultRouter()
recipe_router = DefaultRouter()
tags_router.register(r'tags', TagViewSet, basename='tags')
ingredients_router.register(r'ingredients', IngredientViewSet,
                            basename='ingredients')
user_router.register(r'users', CustomUserViewSet, basename='users')
recipe_router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('', include(user_router.urls)),
    path('', include(tags_router.urls)),
    path('', include(ingredients_router.urls)),
    path('', include(recipe_router.urls)),
]
