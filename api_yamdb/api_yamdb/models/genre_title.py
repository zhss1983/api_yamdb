from django.db import models

from .genre import Genre
from .titles import Titles


class Genre_Title(models.Model):
    #genre = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    #title = models.IntegerField()
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
