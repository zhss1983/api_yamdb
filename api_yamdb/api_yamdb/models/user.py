from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ACCESS_LEVEL = (
        ('U', 'User'),
        ('M', 'Moderator'),
        ('A', 'Admin'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Права',
        max_length=1,
        choices=ACCESS_LEVEL
    )
