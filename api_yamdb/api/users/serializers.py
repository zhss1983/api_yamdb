from random import choice
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api.users.models import Code, User
from api_yamdb.settings import EMAIL_YAMDB


def c_code_generate():
    """
    Генерирует случайную комбинацию букв и цифр
    :return: confirmation_code
    """
    letters = ('abcdefghijkmnopqrstuvwxyz'
               'ABCDEFGHJKLMNOPQRSTUVWXYZ'
               '0123456789')
    return ''.join([choice(letters) for _ in range(30)])


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределяет стандартное поведение
    сериализатора при получении токкена.
    """
    def __init__(self, *args, **kwargs):
        """
        Удаляем поле 'password' из родительского
        класса, чтобы токен можно было получить
        без пароля в запросе.
        """
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields['password']

    # Добавляем новое обязательное поле
    confirmation_code = serializers.CharField(max_length=30, required=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        """Проверяет confirmation_code."""
        username = attrs['username']
        user = get_object_or_404(User, username=username)
        if attrs['confirmation_code'] != user.code.code:
            raise serializers.ValidationError('Wrong confirmation code')
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя не может быть me')
        return value

    def create(self, validated_data):
        """
        Тестовая функция записывает тестовый код
        и дату его создания в БД.
        """
        username = validated_data['username']
        email = validated_data['email']
        c_code = c_code_generate()
        user, _ = User.objects.get_or_create(username=username, email=email)
        print('User is', user.username)
        Code.objects.get_or_create(user_id=user.id, code=c_code)
        send_mail(
            recipient_list=(user.email,),
            from_email=EMAIL_YAMDB,
            subject='Авторизация на нашем сайте',
            message=f'Ваш код для авторизации {c_code}'
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    lookup_field = 'username'

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
