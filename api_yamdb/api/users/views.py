from rest_framework import filters, generics, permissions, status, viewsets
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
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

    def get_object(self):
        """Если пользователь обращается к эндпойнту
        api/v1/users/me/ выводим информацию
        о пользователе, сделавшем запрос."""
        if self.kwargs['username'] == 'me':
            obj = self.request.user
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()

    def get_permissions(self):
        """Если пользователь обращается к эндпойнту
        api/v1/users/me/ даём разрешение на просмотр
        и изменение (частичное и полное) информации.

        -------------------------------------------
        Могли бы здесь запретить и удаление,
        но приходится переопределять код ответа
        сервера
        -------------------------------------------
        """
        if (((self.action == 'retrieve')
             or (self.action == 'partial_update')
             or (self.action == 'update')
             or (self.action == 'destroy'))
                and self.kwargs['username'] == 'me'):
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        """Если пользователь удаляет себя, то
        должен возвращаться код 405 (метод не разрешен),
        а не код 403 (нет прав).
        -------------------------------------------
        Это требование тестов: в задании об этом ничего
        нет, почему не достаточно def get_permissons()
        (выше) не ясно. Ведь дело не в том, что метод
        не разрешен, а в том, что прав пользователя
        для его выполнения не хватает.
        -------------------------------------------
        """
        if request.user.role != 'admin' and kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        """Не даёт пользователю без прав админа поменять
        свою роль.
        """
        if (self.request.user.not_admin
                and 'role' in serializer.validated_data):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()
