from django.db import models

from .genre import Genre
from .title import Title


class Genre_Title(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
