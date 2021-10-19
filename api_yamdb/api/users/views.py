from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import (YAMDBTokenObtainPairSerializer,
                          UserRegistrationSerializer,
                          UserSerializer)


class UserRegistrationViewSet(generics.CreateAPIView):
    """Вьюсет для регистрации новых пользователей."""
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Переопределяет status code: тесты требуют, чтобы
        было 200 ОК. Без этого переопределения возвращается
        201.
        --------------------------------------------------
        Почему так - неясно, мы отправляем POST-запрос и
        создаём новые данные (пользователя, код.)
        --------------------------------------------------
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        super().perform_create(serializer)
        headers = super().get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK, headers=headers)


class YAMBDTokenObtainPairView(TokenObtainPairView):
    """Вьюсет для получения токена. Наследуется от
    вьюсета из Simple JWT.
    """
    serializer_class = YAMDBTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny, )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для операций CRUD с ролью
    администратора, и для CRU только своих учетных
    записей прочими пользователем.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated],
            methods=['PATCH', 'GET'])
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if self.request.user.not_admin and 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')
            serializer.save()
        return Response(serializer.data)
