from django.contrib import admin
from .models import Recipe, Ingredient, Tag, IngredientRecipe

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
        'pk',
        'author',
        'name',
        'text',
        'pub_date',
        'cooking_time'
    )
    
    list_filter = ('pub_date', 'name', 'author')
    empty_value_display = '-пусто-'
    

admin.site.register(Recipe, RecipeAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )


admin.site.register(Ingredient, IngredientsAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )


admin.site.register(Tag, TagAdmin)

