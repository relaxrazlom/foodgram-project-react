from rest_framework import serializers

from recipe.models import (
    Recipe, Tag, Ingredient, Shopping_Cart, Favourite
)


class UserSerializer(serializers.Serializer):

    class Meta:
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'email', 'password'
        )

class RecipeSerializer(serializers.Serializer):

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_fafourite', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'            
        )
        model = Recipe


class TagSerializer(serializers.Serializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.Serializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class ShoppingCartSerializer(serializers.Serializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Shopping_Cart


class FavouriteSerializer(serializers.Serializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favourite