from rest_framework import serializers
from recipes.models import Recipe
from api.models import Tag, Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='slug', queryset=Tag.objects.all(), many=True
    )
    ingredients = serializers.SlugRelatedField(
        slug_field='name', queryset=Ingredient.objects.all(), many=True
    )

    class Meta:
        fields = '__all__'
        model = Recipe
