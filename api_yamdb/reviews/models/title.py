import datetime as dt
from time import strftime

from django.db import models

from .category import Category
from .genre import Genre


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение', max_length=200)
    year = models.IntegerField(
        verbose_name='Год публикации', blank=False)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', through='Genre_Title')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='category',
    )
    description = models.TextField('Описание')

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(year__lte=dt.date.today().year),
                name="year_cannot_be_bigger_then_current"
            ),
        )
