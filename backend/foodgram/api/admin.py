from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingCart)
