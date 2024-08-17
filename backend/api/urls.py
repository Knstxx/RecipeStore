from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (TagViewSet, IngredientViewSet,
                       CustomUserViewSet, RecipeViewSet)


router = DefaultRouter()

router.register(r'tags', TagViewSet,
                basename='tags')
router.register(r'ingredients', IngredientViewSet,
                basename='ingredients')
router.register(r'users', CustomUserViewSet,
                basename='users')
router.register(r'recipes', RecipeViewSet,
                basename='recipe')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
]
