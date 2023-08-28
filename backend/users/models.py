from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    username = models.SlugField(
        unique=True,
        max_length=150,
        verbose_name='Ник'
    )
    email = models.EmailField(
        'E-mail', max_length=254,
        unique=True,
        validators=[validators.validate_email]
    )
    password = models.CharField(
        max_length=150,
        verbose_name='пароль'
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriptionuser'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscription'],
                name='unique_user_subscription'
            ), models.CheckConstraint(
                name='check_self_subscribe',
                check=~models.Q(subscription=models.F('user'))
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.subscription.username}'
