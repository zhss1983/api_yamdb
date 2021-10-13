from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)

from django.shortcuts import get_object_or_404

#from .permissions import IsAuthorOrAnyReadOnly
from .models import Titles, Review

from .serializers import CommentAuthorSerializer, ReviewSerializer


class CommentViewSetAuthor(ModelViewSet):
    serializer_class = CommentAuthorSerializer
    permission_classes = (AllowAny,)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def __get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Titles, pk=title_id)

    def perform_create(self, serializer):
        title = self.__get_title()
        serializer.validated_data['title'] = title
        super().perform_create(serializer)

    def get_queryset(self):
        title = self.__get_title()
        return title.reviews

