from rest_framework import viewsets
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from recipes.serializers import RecipeSerializer, RecipeMakeSerializer
from recipes.models import Recipe
from rest_framework.decorators import action
import random
import string
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class RecipeUrlViewSet(viewsets.ModelViewSet):
    lookup_field = 'short_link'
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create':
            return RecipeMakeSerializer
        return RecipeSerializer

    def get_object(self):
        short_link = self.kwargs.get(self.lookup_field)
        return get_object_or_404(self.get_queryset(),
                                 short_link__contains=short_link)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags', 'is_favorited',
                        'is_in_shopping_cart',)

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create':
            return RecipeMakeSerializer
        return RecipeMakeSerializer

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        if not recipe.short_link:
            baseURL = request.build_absolute_uri('/')
            while True:
                unic_url = ''.join(
                    random.choice(string.ascii_letters
                                  + string.digits) for _ in range(3)
                )
                recipe.short_link = f"{baseURL}s/{unic_url}"
                try:
                    recipe.save()
                    break
                except Exception:
                    continue
        return Response({'short-link': recipe.short_link},
                        status=status.HTTP_200_OK)



'''path('<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(),
         ),
    path('<int:recipe_id>/favorite/',
         FavoriteView.as_view(),
         ),'''


class DownloadCartView(APIView):
    pass
