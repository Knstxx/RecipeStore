from rest_framework import serializers
from recipes.models import Recipe, RecipeIngredient
from drf_extra_fields.fields import Base64ImageField
from api.models import Tag, Ingredient
from users.serializers import CustomUserSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']

class RecipeMakeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = RecipeIngredientSerializer(
        many=True
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    '''is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()'''

    class Meta:
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
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
        breakpoint()
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )
        if tags is not None:
            recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        if tags is not None:
            instance.tags.set(tags)
        instance.ingredients.clear()
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=instance,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )
        instance.save()
        return instance


class RecipeSerializer(RecipeMakeSerializer):

    class Meta:
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']
        model = Recipe
