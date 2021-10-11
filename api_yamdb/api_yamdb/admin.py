from django.contrib import admin

from .models import Category, Comment, Genre, Review, Titles

EMPTY = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('-pub_date', 'author')
    empty_value_display = EMPTY


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('-pub_date', 'author')
    empty_value_display = EMPTY


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'rating', 'genre', 'category')
    search_fields = ('name', 'year', 'genre__name', 'category__name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Titles, TitlesAdmin)
