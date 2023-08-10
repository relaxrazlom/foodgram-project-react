from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Тег'
    )
    color = models.CharField(
        unique=True,
        max_length=30,
        verbose_name='Цвет')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Ингредиенты'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name="Единица измерения"
    )
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
    ) 
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe/images/',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Текстовое описание')
    pub_date = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(360)],
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты к рецепту'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000000)
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Выбор Ингредиента'
        verbose_name_plural = 'Выбор Ингредиента'


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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites_user'
    )
    favourites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites'
    )


class Shopping_Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user'
    )
    favourites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
