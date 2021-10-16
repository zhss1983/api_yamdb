from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.models import User
from .permissions import IsAdmin
from .serializers import (MyTokenObtainPairSerializer,
                          UserRegistrationSerializer,
                          UserSerializer)


class UserRegistrationViewSet(viewsets.ModelViewSet):  # Подобрать подходящий Миксин на создание
    """Вьюсет для регистрации новых пользователей."""
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class MyTokenObtainPairView(TokenObtainPairView):
    """Вьюсет для получения токена. Наследуется от
    вьюсета из Simple JWT.
    """
    serializer_class = MyTokenObtainPairSerializer
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
        if (((self.action == 'retrieve') or
             (self.action == 'partial_update') or
             (self.action == 'update') or
             (self.action == 'destroy'))
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
        if (self.request.user.role != 'admin' and
                'role' in serializer.validated_data):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer.save()

