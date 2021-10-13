from django import forms

from django.contrib import admin

from .models import Category, Comment, Genre, Review, Titles, User

EMPTY = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    empty_value_display = EMPTY


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    empty_value_display = EMPTY


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'year')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role')
    search_fields = ('username',)

    def save_model(self, request, obj, form, change):
        """
        Перехватывает строку из админки, шифрует
        пароль. Без переопределения функции, пароль
        сохраняется в БД в виде нешифрованной строки.
        """
        str_password = obj.password
        obj.set_password(str_password)
        obj.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(User, UsersAdmin)
