from rest_framework.routers import DefaultRouter
from django.urls import include, path

from recipes.views import (RecipeViewSet, GetLinkView, DownloadCartView,
                           FavoriteView, ShoppingCartView)


recipes_router = DefaultRouter()
recipes_router.register(r'', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(recipes_router.urls)),
    path('download_shopping_cart/',
         DownloadCartView.as_view(),
         name='d-shopping-cart'
         ),
    path('<int:recipe_id>/get-link/',
         GetLinkView.as_view(),
         name='get-link'
         ),
    path('<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(),
         name='get-link'
         ),
    path('<int:recipe_id>/favorite/',
         FavoriteView.as_view(),
         name='get-link'
         ),
]
