from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ACCESS_LEVEL = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(
        'Права',
        max_length=9,
        choices=ACCESS_LEVEL,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
