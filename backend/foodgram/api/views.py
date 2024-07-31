from rest_framework import viewsets

from api.serializers import TagSerializer, IngredientSerializer
from api.models import Tag, Ingredient


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
