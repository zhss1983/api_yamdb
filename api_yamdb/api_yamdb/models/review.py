from django.db import models

from users.models import User
from .title import Title


class Review(models.Model):
    #title = models.IntegerField()
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    text = models.TextField('Отзыв')
    #author = models.IntegerField()
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField('Оценка', default=5, blank=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:15]
