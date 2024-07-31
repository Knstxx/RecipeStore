from django.contrib import admin

from api.models import Tag, Ingredient
from recipes.models import Recipe, RecipeIngredient, RecipeTag

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
