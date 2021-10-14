from django.db.models import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title

SCORE_VALIDATION_ERROR_MESSAGE = ('Оценка должна быть числом целым в диапазоне'
                                  ' от 0 до 10.')

class CommentAuthorSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review

<<<<<<< Updated upstream
class TitleSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title

=======
>>>>>>> Stashed changes
    def validate_score(self, value):
        if not (isinstance(value, int) and 0 <= value <= 10):
            raise ValidationError(SCORE_VALIDATION_ERROR_MESSAGE)
        return value

class TitleSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
