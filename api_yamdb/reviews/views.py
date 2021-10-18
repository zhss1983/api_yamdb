from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django.shortcuts import get_object_or_404

from .permissions import EditAccessOrReadOnly, AdminOrReadOnly
from api_yamdb.reviews.models import Title, Genre, Category
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleSerializer)
from .filters import TitleFilter


class GetTitleBaseViewSet(ModelViewSet):
    permission_classes = (EditAccessOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class GetReviewBaseViewSet(GetTitleBaseViewSet):

    def get_review(self):
        title = self.get_title()
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(title.reviews, pk=review_id)


class ReviewViewSet(GetTitleBaseViewSet):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(GetReviewBaseViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)


class CategoryGenreViewSet(CreateModelMixin,
                           DestroyModelMixin,
                           ListModelMixin,
                           GenericViewSet):
    """Base ViewSet class for GenreViewSet and CategoryViewSet"""
    permission_classes = (AdminOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
