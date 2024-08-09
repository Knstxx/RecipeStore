from django.contrib import admin

from api.models import Tag, Ingredient
from recipes.models import Recipe, Favorite, ShopCard
from users.models import User, Subscribe

admin.site.register(Tag)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'measurement_unit']


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['author', 'name']
    readonly_fields = ['favorite_count']
    list_filter = ['tags']
    list_display = ['name', 'get_author_name']

    def favorite_count(self, obj):
        return obj.favorites.count()
    favorite_count.short_description = 'Число добавлений в избранное'

    def get_author_name(self, obj):
        return obj.author.username
    get_author_name.short_description = 'Автор'


admin.site.register(Recipe, RecipeAdmin)


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'username']


admin.site.register(User, UserAdmin)

admin.site.register(Favorite)

admin.site.register(ShopCard)

admin.site.register(Subscribe)
