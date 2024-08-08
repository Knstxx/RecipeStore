from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from recipes.serializers import (RecipeSerializer, RecipeMakeSerializer,
                                 FavShopSerializer)
from recipes.models import Recipe, Favorite, ShopCard
from rest_framework.decorators import action
import random
import string
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from collections import defaultdict
from fpdf import FPDF
from django.http import HttpResponse
import io


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
    filterset_fields = ('author', 'tags',)

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create':
            return RecipeMakeSerializer
        return RecipeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1' and user.is_authenticated:
            queryset = queryset.filter(favorites__user=user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart == '1' and user.is_authenticated:
            queryset = queryset.filter(inshop_cart__user=user)
        return queryset

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

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже у вас в избранном.'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavShopSerializer(recipe,
                                           context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт не находится у вас в избранном.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if ShopCard.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже у вас в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST)
            ShopCard.objects.create(user=user, recipe=recipe)
            serializer = FavShopSerializer(recipe,
                                           context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            shop_cart = ShopCard.objects.filter(user=user, recipe=recipe)
            if shop_cart.exists():
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт не находится у вас в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='download_shopping_cart')
    def download_cart(self, request):
        user = request.user
        rec_in_cart = ShopCard.objects.filter(
            user=user).prefetch_related('recipe__ingredients')
        ingredients = defaultdict(int)
        for item in rec_in_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                ingredient = recipe_ingredient.ingredient
                ingredients[(ingredient.name,
                             ingredient.measurement_unit)
                            ] += recipe_ingredient.amount

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.add_font('ComicSansMS', '',
                     'recipes/fonts/ComicSansMS.ttf',
                     uni=True)
        pdf.add_font('ComicSansMSB', '',
                     'recipes/fonts/ComicSansMSB.ttf',
                     uni=True)
        pdf.set_text_color(0, 181, 134)
        pdf.set_font("ComicSansMSB", size=25)
        pdf.cell(0, 10, "К закупкам!", ln=True, align='C')
        pdf.set_text_color(0, 45, 143)
        pdf.set_font("ComicSansMS", size=14)
        for index, ((name, unit), amount) in enumerate(ingredients.items()):
            line_text = f"{index + 1}. {name} ({unit}) — {amount}"
            pdf.cell(0, 10, line_text, ln=True)
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        response = HttpResponse(pdf_output, content_type='application/pdf')
        response['Content-Disposition'
                 ] = 'attachment; filename="shopping_cart.pdf"'
        return response
