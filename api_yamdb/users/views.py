from rest_framework import mixins, viewsets

from .models import User
from .serializers import UserRegisterSerializer


class UserRegisterViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
