from rest_framework import filters, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.models import User
from .permissions import IsAdmin
from .serializers import MyTokenObtainPairSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
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
        api/v1/users/me/ даём разрешение на получение
        информации и полное и частичное обновление
        информации о себе.
        """
        if ((self.action == 'retrieve') or
                (self.action == 'partial_update') or
                (self.action == 'update') and
                self.kwargs['username'] == 'me'):
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()
