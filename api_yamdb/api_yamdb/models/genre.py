from django.db import models

class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=200, unique=True)
    slug = models.SlugField(verbose_name='Адрес жанра', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name
