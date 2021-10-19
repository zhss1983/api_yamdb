from django.db import models
from django.utils import timezone

from .category import Category
from .genre import Genre


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение', max_length=200, db_index=True)
    year = models.IntegerField(
        verbose_name='Год публикации', blank=False, db_index=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='titles',
    )
    description = models.TextField('Описание')

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year),
                name='year_cannot_be_bigger_then_current'
                # Данный метод работает, проверено.
                # INSERT INTO reviews_title (category_id, description, year,
                # name, id ) VALUES (1, '', 2022, 'Побег из Шоушенка 2', 1);
                # [20:23:43] Ошибка при выполнении SQL запроса к базе данных
                # 'yamdb': CHECK constraint failed:
                # year_cannot_be_bigger_then_current
            ),
        )
