from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from recipes.serializers import RecipeSerializer, RecipeMakeSerializer
from recipes.models import Recipe
from rest_framework.response import Response


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags', 'is_favorited',
                        'is_in_shopping_cart',)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeMakeSerializer
        return RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        recipe_id = self.kwargs.get('pk')
        return Recipe.objects.filter(id=recipe_id)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return RecipeMakeSerializer
        return RecipeSerializer


'''class GetLinkView(APIView):
    pass

class DownloadCartView(APIView):
    pass


class FavoriteView(APIView):
    pass
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
         ),'''


class DownloadCartView(APIView):
    pass
