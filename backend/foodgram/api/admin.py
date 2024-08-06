from django.contrib import admin

from api.models import Tag, Ingredient
from recipes.models import Recipe
from users.models import User

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(User)
