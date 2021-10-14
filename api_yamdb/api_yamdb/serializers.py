from rest_framework import serializers
from django.db.models import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from .models import Category, Comment, Genre, Review, Title, Genre_Title

SCORE_VALIDATION_ERROR_MESSAGE = ('Оценка должна быть числом целым в диапазоне'
                                  ' от 0 до 10.')

class CommentSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment
        read_only_fields = ('author', )


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category


class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review
        read_only_fields = ('author', )

    def validate_score(self, value):
        if not (isinstance(value, int) and 0 <= value <= 10):
            raise ValidationError(SCORE_VALIDATION_ERROR_MESSAGE)
        return value


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'rating', 'genre', 'category')
        #read_only_fields = ('rating', 'category', 'genre') # Не работет

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if rating:
            return round(rating, 2)
        return 'Оценки пока нет'

    def create(self, validated_data):
        genres = self.initial_data.pop('genre')
        genres_list = tuple(get_object_or_404(Genre, slug=genre) for genre in genres)
        category = get_object_or_404(Category, slug=self.initial_data.pop('category'))
        title = Title.objects.create(**validated_data, category=category)
        for genre in genres_list:
            Genre_Title.objects.get_or_create(title=title, genre=genre)
        return title