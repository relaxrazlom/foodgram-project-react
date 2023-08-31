from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Тег'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цвет')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиенты'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe/',
        verbose_name='Изображение',
        blank=False
    )
    text = models.TextField(verbose_name='Текстовое описание')
    pub_date = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Ингредиенты к рецепту'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Выбор Ингредиента'
        verbose_name_plural = 'Выбор Ингредиента'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Выбор Тега'
        verbose_name_plural = 'Выбор Тега'

    def __str__(self):
        return f'{self.recipe}: {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favoritesuser'
    )
    favorites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Добавлено в избранное',
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorites'],
                name='unique_user_favorites'
            )
        ]

    def __str__(self):
        return '{self.user}: {self.recipe}'


class Shopping_Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shoppinguser'
    )
    favorites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Добавлено в корзину',
        related_name='shoppingcart'
    )

    class Meta:
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorites'],
                name='unique_user_shopping_cart'
            )
        ]

    def __str__(self):
        return '{self.user}: {self.recipe}'
