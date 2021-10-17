from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    """Кастомная модель пользователя с доплнительными полями 'role' и 'bio'."""
    ACCESS_LEVEL = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
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

    # Необходимо для того, чтобы при создании
    # пользователя через консоль, запрашивался
    # email
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Code(models.Model):
    """Модель для хранения confirmation code
    пользователя.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='code',
        verbose_name='Пользователь',
        primary_key=True
    )
    code = models.CharField(
        max_length=30,
        verbose_name='confirmation_code'
    )
