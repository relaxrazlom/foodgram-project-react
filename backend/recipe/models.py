from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import User


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
    score = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

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
    ingridients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(360)],
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('pub_date',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
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
        related_name='user'
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
        related_name='user'
    )
    favourites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
