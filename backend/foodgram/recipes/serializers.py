from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient
from api.models import Tag


class RecipeIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class RecipeMakeSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='id', queryset=Tag.objects.all(), many=True
    )
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True
    )
    '''is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()'''

    class Meta:
        fields = ['ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time']
        model = Recipe

    '''def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False'''

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        tags_data = validated_data.pop('tags')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        tags_data = validated_data.pop('tags')
        super().update(instance, validated_data)
        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        instance.tags.set(tags_data)
        return instance


class RecipeSerializer(RecipeMakeSerializer):

    class Meta:
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']
        model = Recipe
