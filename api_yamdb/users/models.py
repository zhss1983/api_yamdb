from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    ACCESS_LEVEL = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(
        'Права',
        max_length=1,
        choices=ACCESS_LEVEL
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = CustomUserManager()

    def __str__(self):
        return self.username
