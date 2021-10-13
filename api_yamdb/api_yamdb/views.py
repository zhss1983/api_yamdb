from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (
    GenericViewSet, ModelViewSet, ReadOnlyModelViewSet)

from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrModeratorOrReadOnly
from .models import Titles, Review
from .serializers import CommentAuthorSerializer, ReviewSerializer, TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def __get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Titles, pk=title_id)

    def perform_create(self, serializer):
        title = self.__get_title()
        serializer.validated_data['title'] = title
        super().perform_create(serializer)

    def get_queryset(self):
        title = self.__get_title()
        return title.reviews.all()

class CommentViewSetAuthor(ReviewViewSet):
    serializer_class = CommentAuthorSerializer

    def __get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def perform_create(self, serializer):
        title = self.__get_title()
        review = self.__get_review()
        serializer.validated_data['title'] = title
        super().perform_create(serializer)

    def get_queryset(self):
        title = self.__get_title()
        return title.reviews.all()
