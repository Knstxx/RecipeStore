from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import TagViewSet, IngredientViewSet


tags_router = DefaultRouter()
ingredients_router = DefaultRouter()
tags_router.register(r'tags', TagViewSet, basename='tags')
ingredients_router.register(r'ingredients', IngredientViewSet,
                            basename='ingredients')

urlpatterns = [
    path('',
         include(tags_router.urls)
         ),
    path('',
         include(ingredients_router.urls)
         ),
    path('', include('users.urls')),
]
