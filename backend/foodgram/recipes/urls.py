from django.urls import path

from recipes.views import RecipesViewSet, RecipeViewSet, DownloadCartView


urlpatterns = [
    path('<int:pk>/',
         RecipeViewSet.as_view({'get': 'list',
                                'patch': 'partial_update',
                                'delete': 'destroy'}),
         name='recipe'
         ),
    path('',
         RecipesViewSet.as_view({'get': 'list',
                                 'post': 'create'}),
         name='recipes'
         ),
    path('download_shopping_cart/',
         DownloadCartView.as_view(),
         name='d-shopping-cart'
         ),
]
