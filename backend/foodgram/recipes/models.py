from django.db import models
from users.models import User
from api.models import Tag, Ingredient
import base64
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator


class Base64ImageField(models.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='authors')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    name = models.CharField(max_length=256)
    image = Base64ImageField(upload_to='recipe_images',
                             null=True, blank=True)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

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
