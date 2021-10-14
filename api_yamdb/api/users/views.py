from django.shortcuts import get_object_or_404

from rest_framework import filters, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.models import User
from .permissions import IsAdmin
from .serializers import MyTokenObtainPairSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        if self.kwargs['username'] == 'me':
            queryset = User.objects.filter(id=self.request.user.id)
            return queryset
        return User.objects.all()

    # Прописать разрешения прав для не администраторов

    # def get_permissions(self):
    #     if (self.action == 'retrieve' and
    #             self.kwargs['username'] == 'me'):
    #         print('retrieve', self.kwargs)
    #     if (self.action == 'partial_update' and
    #             self.kwargs['username'] == 'me'):
    #         print('partial_update', self.kwargs)
    #     return super().get_permissions()
