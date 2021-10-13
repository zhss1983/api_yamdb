from django.db import models

from .category import Category
from .genre import Genre


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение', max_length=200)
    year = models.DateTimeField(
        verbose_name='Год публикации', blank=False)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', through='Genre_Title')
    # category = models.IntegerField()
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='category',
    )
