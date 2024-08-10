from rest_framework import serializers
from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from users.models import User, Subscribe
from recipes.models import Recipe


class RecipeSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CreateUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password')

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Пароль должен содержать не менее 6 символов.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'email': representation['email'],
            'id': instance.id,
            'username': representation['username'],
            'first_name': representation['first_name'],
            'last_name': representation['last_name'],
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class SubSerializer(CustomUserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('recipes_count',
                                                     'recipes',)

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj).order_by('-id')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeSubSerializer(recipes, many=True,
                                   context={'request': request}).data
