from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from recipe.models import (
    Recipe, Tag, Ingredient, Shopping_Cart, IngredientRecipe, Favorite
)
from users.models import User, Subscribe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.id:
            return False
        if Subscribe.objects.filter(user=user, subscription=obj).values():
            return True
        return False


class RecipeSubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField(source='subscription.id')
    first_name = serializers.ReadOnlyField(source='subscription.first_name')
    last_name = serializers.ReadOnlyField(source='subscription.last_name')
    username = serializers.ReadOnlyField(source='subscriptionr.username')
    email = serializers.ReadOnlyField(source='subscription.email')

    class Meta:
        model = Subscribe
        fields = (
            'id', 'first_name', 'last_name',
            'username', 'email', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.subscription.recipes.count()

    def get_recipes(self, obj):
        return RecipeSubscriptionsSerializer(
            obj.subscription.recipes.all(), many=True
        ).data

    def get_is_subscribed(self, obj):
        return True


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeReadSerializer(
        read_only=True, many=True, source='ingredientrecipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.id:
            return False
        if Favorite.objects.filter(user=user, favorites=obj).values():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.id:
            return False
        if Shopping_Cart.objects.filter(user=user, favorites=obj).values():
            return True
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'tags', 'ingredients', 'image',
            'name', 'text', 'cooking_time'
        )
        model = Recipe

    def _create_ingredients(self, recipe, ingredients):

        obj = (IngredientRecipe(
            ingredient_id=ingredient['id'],
            amount=ingredient['amount'],
            recipe=recipe
        ) for ingredient in ingredients)
        IngredientRecipe.objects.bulk_create(obj)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        self._create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = self.initial_data.pop('ingredients')
        IngredientRecipe.objects.filter(recipe=instance).all().delete()
        self._create_ingredients(instance, ingredients)
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        instance.image = validated_data['image']
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data


class FavoritesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='favorites.id')
    name = serializers.ReadOnlyField(source='favorites.name')
    image = serializers.ImageField(read_only=True, source='favorites.image')
    cooking_time = serializers.ReadOnlyField(source='favorites.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='favorites.id')
    name = serializers.ReadOnlyField(source='favorites.name')
    image = serializers.ImageField(read_only=True, source='favorites.image')
    cooking_time = serializers.ReadOnlyField(source='favorites.cooking_time')

    class Meta:
        model = Shopping_Cart
        fields = ('id', 'name', 'image', 'cooking_time')
