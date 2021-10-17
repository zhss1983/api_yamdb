from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField)

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.http import QueryDict

from .models import Category, Comment, Genre, Review, Title, Genre_Title


class GetDefault:
    """Base class for get default values"""
    requires_context = True

    def __call__(self, serializer_field):
        pass

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class GetTitle(GetDefault):
    """Get Title grantee from id in url or 404"""
    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title


class GetReview(GetDefault):
    """Get Review grantee from id in url or 404"""
    def __call__(self, serializer_field):
        title = GetTitle()(serializer_field)
        review_id = serializer_field.context['view'].kwargs.get('review_id')
        return get_object_or_404(title.reviews, pk=review_id)


class CommentSerializer(ModelSerializer):
    review = serializers.HiddenField(default=GetReview())
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment
        read_only_fields = ('id', )


class MetaGenreCategore:
    """Base Meta class for GenreSerializer and CategorySerializer"""
    fields = ('name', 'slug')
    lookup_field = 'slug'
    extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(ModelSerializer):
    class Meta(MetaGenreCategore):
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta(MetaGenreCategore):
        model = Category


class ReviewSerializer(ModelSerializer):
    SCORE_ERROR = 'Оценка должна быть числом целым в диапазоне от 0 до 10.'

    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())
    title = serializers.HiddenField(default=GetTitle())

    class Meta:
        UNIQUE_ERROR = 'Одно произведение, один отзыв, не более.'
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('id', 'author', )
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=UNIQUE_ERROR
            ),
        )

    def validate_score(self, value):
        if not (isinstance(value, int) and 0 <= value <= 10):
            raise ValidationError(self.SCORE_ERROR)
        return value


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=False)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category')
        read_only_fields = ('id', 'rating', 'genre', 'category')

    def get_rating(self, obj):
        """Calculates the average rating based on reviews."""
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if rating:
            return round(rating, 2)
        return None


    def category_getting(self):
        """Category access granted or 404"""
        slug = self.initial_data.get('category')
        return get_object_or_404(Category, slug=slug)

    def genre_save(wrapper_method):
        """Genres access granted or 404"""
        def wrapper(self, *args):
            if isinstance(self.initial_data, QueryDict):
                genres = self.initial_data.getlist('genre')
            else:
                genres = self.initial_data.get('genre')
            genres_list = tuple(
                get_object_or_404(Genre, slug=genre) for genre in genres)
            instance = wrapper_method(self, *args)
            for genre in genres_list:
                Genre_Title.objects.get_or_create(title=instance, genre=genre)
            return instance
        return wrapper

    @genre_save
    def create(self, validated_data):
        return Title.objects.create(
            **validated_data, category=self.category_getting())

    @genre_save
    def update(self, instance, validated_data):
        instance.category = self.category_getting()
        for attr, value in validated_data.items():
            if attr not in ['category', 'genre']:
                setattr(instance, attr, value)
        instance.save()
        return instance
