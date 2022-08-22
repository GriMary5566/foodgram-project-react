from django.contrib.auth.models import AbstractUser
from django.db import models


class EmailLoginUser(AbstractUser):
    password = models.CharField(
        'Пароль',
        max_length=150,
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'Пользователь {self.email}'


User = EmailLoginUser


class Follow(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='following'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='follow_unique',
            ),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.following}"
