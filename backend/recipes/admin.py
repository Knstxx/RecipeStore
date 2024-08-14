from django.contrib import admin

from recipes.models import Recipe, Favorite, ShopCard, Tag, Ingredient

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
admin.site.register(Favorite)
admin.site.register(ShopCard)
