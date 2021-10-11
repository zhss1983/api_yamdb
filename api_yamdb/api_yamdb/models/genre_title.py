from django.db import models

from .genre import Genre
from .titles import Titles


class Genre_Title(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)