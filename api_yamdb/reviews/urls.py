from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    CommentViewSet,
                    GenreViewSet,
                    ReviewViewSet,
                    TitleViewSet)
from api.users.views import (MyTokenObtainPairView,
                             UserRegistrationViewSet,
                             UserViewSet)

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
    'auth/signup',
    UserRegistrationViewSet,
    basename='signup'
)
# r'posts/(?P<post_id>\d+)/
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
]