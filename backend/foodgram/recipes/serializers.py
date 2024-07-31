from rest_framework import serializers
from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Recipe
