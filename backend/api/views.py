from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import TagSerializer, IngredientSerializer
from api.models import Tag, Ingredient
from api.filters import IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    http_method_names = ['get']
