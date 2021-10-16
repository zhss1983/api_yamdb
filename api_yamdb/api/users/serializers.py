from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.users.models import Code, User


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""
    class Meta:
        model = User
        fields = ('email', 'username')

    def create(self, validated_data):
        """Тестовая функция записывает тестовый код
        и дату его создания в БД.

        ---
        ToDo: Сделать отправку на email
        ToDo: Сделать кодировку confirmation_code
        """
        username = validated_data['username']
        email = validated_data['email']
        c_code = 'some-random-code'
        user, _ = User.objects.get_or_create(username=username, email=email)
        code_obj = Code.objects.get_or_create(user_id=user.id, code=c_code)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя.
    TODO: сделать read_only для role
    """
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