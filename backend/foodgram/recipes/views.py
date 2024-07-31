from rest_framework import viewsets
from rest_framework.views import APIView

from recipes.serializers import RecipeSerializer
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class GetLinkView(APIView):
    pass


class DownloadCartView(APIView):
    pass


class FavoriteView(APIView):
    pass


class ShoppingCartView(APIView):
    pass
