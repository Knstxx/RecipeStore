from django_filters import rest_framework as filters

from recipes.models import Ingredient, Tag
from recipes.models import Recipe


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',
                              method='filter_by_name',)

    class Meta:
        model = Ingredient
        fields = ['name']

    def filter_by_name(self, queryset, name, value):
        res = queryset.filter(name__istartswith=value)
        if res.exists():
            return res
        return queryset.filter(name__icontains=value.lower())


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(inshop_cart__user=user)
        return queryset
