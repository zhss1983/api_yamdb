from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from rest_framework import generics, mixins, views

from django.shortcuts import get_object_or_404

from .permissions import EditAccessOrReadOnly, AdminOrReadOnly, AdminOrModeratorOrReadOnly
from .models import Title, Review, Genre, Category
from .serializers import CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer, TitleSerializer


class GetTitleBaseViewSet(ModelViewSet):
    permission_classes = (EditAccessOrReadOnly, )
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
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

class CommentViewSet(GetReviewBaseViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (
        AdminOrReadOnly,
#        AllowAny,
#        EditAccessOrReadOnly,
#        AdminOrModeratorOrReadOnly,
    )
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']


class GenreViewSet(
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        AdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'

class CategoryViewSet(
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        AdminOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination
    filter_backends =(filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'