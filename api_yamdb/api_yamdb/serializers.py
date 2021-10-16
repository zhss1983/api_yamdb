from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from .models import Category, Comment, Genre, Review, Title, Genre_Title

SCORE_VALIDATION_ERROR_MESSAGE = ('Оценка должна быть числом целым в диапазоне'
                                  ' от 0 до 10.')

class CommentSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'author', )


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        return super().update(instance, validated_data)



class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'author', )


    def validate_score(self, value):
        if not (isinstance(value, int) and 0 <= value <= 10):
            raise ValidationError(SCORE_VALIDATION_ERROR_MESSAGE)
        return value


class TitleSerializer(ModelSerializer):
    id = serializers.IntegerField(source='pk', required=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'rating', 'genre', 'category')
        read_only_fields = ('id', 'rating', 'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if rating:
            return round(rating, 2)
        return None

    def validate_category(self, value):
        print(value)
        return value


    def category(self):
        instance = get_object_or_404(
            Category, slug=self.initial_data.get('category'))
        print(instance)
        return instance


    def create(self, validated_data):
        #        return self.create_title(validated_data)
        genres = self.initial_data.getlist('genre')
        genres_list = tuple(
            get_object_or_404(Genre, slug=genre) for genre in genres)
#        instance = Title.objects.create(**validated_data) # , category=self.category()
        instance = Title.objects.create(**validated_data, category=self.category())
        for genre in genres_list:
            Genre_Title.objects.get_or_create(title=instance, genre=genre)
        return instance


    def update(self, instance, validated_data):
        #        return self.update_title(instance, validated_data)
        genres = self.initial_data.getlist('genre')
        genres_list = tuple(
            get_object_or_404(Genre, slug=genre) for genre in genres)
        instance.category = self.category()
        print(instance.save)
        for genre in genres_list:
            Genre_Title.objects.get_or_create(title=instance, genre=genre)
        return instance


"""
    def genre(title_function):
        def genre_update():
            def wrapper(*args, **kwargs):
                print(args)
                print(kwargs)
                self = 1
                genres = self.initial_data.getlist('genre')
                genres_list = tuple(
                    get_object_or_404(Genre, slug=genre) for genre in genres)
                instance = title_function(self, *args, **kwargs)
                for genre in genres_list:
                    Genre_Title.objects.get_or_create(title=instance,
                                                      genre=genre)
                return instance
            print('I\'m coming genre update')
            return wrapper
        print('I\'m coming')
        return genre_update
        
        
        
        
        
    @genre
    def create_title(self, validated_data):
        title = Title.objects.create(
            **validated_data, category=self.category())
        return title
    @genre
    def update_title(self, instance, validated_data):
        instance.category = self.category()
        print(instance.save)
        return instance
        
        
        
        
        
        
        
        
        
        
        
        

def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end - start))
        return return_value

    return wrapper


@benchmark
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text


webpage = fetch_webpage('https://google.com')
print(webpage)
"""