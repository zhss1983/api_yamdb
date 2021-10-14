from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

ACCESS_LEVEL = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin')
)


class User(AbstractUser):
    role = models.CharField(
        'Права',
        max_length=1,
        choices=ACCESS_LEVEL,
        default='user'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
