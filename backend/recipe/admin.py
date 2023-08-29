from django.contrib import admin

from .models import (
    Recipe, Ingredient, Tag, IngredientRecipe, Favorite, Shopping_Cart
)


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    verbose_name = 'Ингредиент'


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1
    verbose_name = 'Тег'


class RecipeAdmin(admin.ModelAdmin):
    inlines = [TagInline, IngredientsInLine]
    list_display = (
        'author',
        'name',
        'count_to_favorites'
    )
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags')
    search_fields = (
        'name',
        'author__username',
        'tags__slug',
        'tags__name'
    )

    @admin.display(description='Добавлено в избранное')
    def count_to_favorites(self, obj: Recipe):
        return obj.favorites.count()


admin.site.register(Recipe, RecipeAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientsAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('color', 'slug')
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_editable = ('amount',)


admin.site.register(IngredientRecipe, IngredientRecipeAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'favorites'
    )


admin.site.register(Favorite, FavoriteAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'favorites'
    )


admin.site.register(Shopping_Cart, ShoppingCartAdmin)
