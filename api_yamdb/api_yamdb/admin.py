from django.contrib import admin

<<<<<<< HEAD
from users.models import User

from .models import Category, Comment, Genre, Review, Title
=======
from .models import Category, Comment, Genre, Review, Title, User
>>>>>>> f7b44bc (Добавил вьюсет для произведений, пофиксил Titles - Title в некоторых файлах)

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


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description')
    search_fields = ('name', 'year')


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role')
    search_fields = ('username', )

    def save_model(self, request, obj, form, change):
        """
        Добавляет шифрование пароля при создании
        пользователя через админку. Без переопределения
        метода пароль в БД хранится в виде строки.
        """
        obj.set_password(obj.password)
        obj.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
