from django.db import models

class Category(models.Model):
    name = models.CharField('Категория', max_length=200, unique=True)
    slug = models.SlugField('Адрес категории', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name
