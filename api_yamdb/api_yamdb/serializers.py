from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Titles


class CommentAuthorSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = ['text', 'author', 'score', 'pub_date']
        model = Review

    # Повесить валидатор на score