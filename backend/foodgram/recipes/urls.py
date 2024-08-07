from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet, DownloadCartView


recipe_router = DefaultRouter()
recipe_router.register(r'recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(recipe_router.urls)),
    path('download_shopping_cart/',
         DownloadCartView.as_view(),
         name='d-shopping-cart'
         ),
]
