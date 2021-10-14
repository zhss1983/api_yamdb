from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, BasePermission, AllowAny

from django.shortcuts import get_object_or_404

from .permissions import EditAccessOrReadOnly
from .models import Title, Review
from .serializers import CommentSerializer, ReviewSerializer, TitleSerializer


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
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
