from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.users.models import User, ACCESS_LEVEL


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Переопределяет стандартное поведение
     сериализатора при получении токкена.
     """
    def __init__(self, *args, **kwargs):
        """Удаляем поле 'password' из родительского
        класса, чтобы токен можно было получить
        без пароля в запросе.
        """
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields['password']

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        username = attrs['username']
        user = User.objects.get(username=username)
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class StringToSymbol(serializers.Field):
    """Преобразовывает значение хранящееся в БД
    в виде одного символа, в слово.
    """
    def to_representation(self, value):
        for level in ACCESS_LEVEL:
            symbol, role = level
            if value == symbol:
                return role
        return value

    def to_internal_value(self, data):
        role_list = []
        for level in ACCESS_LEVEL:
            role_list.append(level[1])
        if data not in role_list:
            raise serializers.ValidationError(
                'No such user role'
            )
        data = data[:1]
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""
    role = StringToSymbol(required=False)
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

class AuthSignup(serializers.Serializer):
    email = serializers.EmailField()
    usernsme = serializers.CharField()

