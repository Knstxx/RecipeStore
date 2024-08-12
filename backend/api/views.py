import io
import random
import string

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from collections import defaultdict
from fpdf import FPDF
from django.http import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet

from api.serializers import TagSerializer, IngredientSerializer
from recipes.models import Tag, Ingredient, Recipe, Favorite, ShopCard
from users.models import User, Subscribe
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReaderOrAuthenticated
from api.serializers import (RecipeSerializer, RecipeMakeSerializer,
                             FavShopSerializer, CustomUserSerializer,
                             CreateUserSerializer, SubSerializer)


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
    permission_classes = [IsAuthorOrReaderOrAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'partial_update' or self.action == 'create':
            return RecipeMakeSerializer
        return RecipeSerializer

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

    @action(detail=False, methods=['get'], url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_cart(self, request):
        user = request.user
        rec_in_cart = ShopCard.objects.filter(
            user=user).prefetch_related('recipe__ingredients')
        if not rec_in_cart.exists():
            return Response({"detail": "Корзина пуста"},
                            status=status.HTTP_200_OK)
        ingredients = defaultdict(int)
        print(rec_in_cart)
        for item in rec_in_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                ingredient = recipe_ingredient.ingredient
                ingredients[(ingredient.name, ingredient.measurement_unit)
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


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = CustomUserSerializer(paginated_users,
                                          context={'request': request},
                                          many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['put', 'delete'], url_path='me/avatar')
    def set_avatar(self, request, *args, **kwargs):
        user = request.user

        if request.method == 'PUT':
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'avatar': serializer.data.get('avatar')})
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user.avatar.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscribe(self, request, id=None):
        author = self.get_object()
        user = request.user

        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписаться на себя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription = Subscribe.objects.filter(user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='subscriptions',
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscribe.objects.filter(user=user)
        authors = [subscription.author for subscription in subscriptions]
        paginator = self.pagination_class()
        paginated_authors = paginator.paginate_queryset(authors, request)
        serializer = SubSerializer(paginated_authors,
                                   context={'request': request},
                                   many=True)
        return paginator.get_paginated_response(serializer.data)
