from django.db import models
from users.models import User
from api.models import Tag, Ingredient
from django.core.validators import MinValueValidator

from recipes.fields import Base64ImageField


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        blank=False
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authors')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        blank=False
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(max_length=256,
                            null=False, blank=False)
    image = Base64ImageField(upload_to='recipe_images',
                             null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        null=False, blank=False
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tags_recipes'
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
