from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия'
    )
    username = models.SlugField(
        unique=True,
        verbose_name='Ник')
    email = models.EmailField(
        'E-mail', max_length=254, unique=True, blank=True)
    password = models.CharField(
        max_length=30,
        verbose_name='пароль'
    )
