from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet)
from api.users.views import (
    MyTokenObtainPairView, UserRegistrationViewSet, UserViewSet)

api_router_v1 = DefaultRouter()
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
api_router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
api_router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
api_router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
api_router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('v1/', include(api_router_v1.urls)),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', UserRegistrationViewSet.as_view(),
         name='token_obtain_pair'
         ),
]
