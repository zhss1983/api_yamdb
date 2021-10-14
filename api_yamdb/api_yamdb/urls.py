from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.users.views import UserViewSet
from .views import CommentViewSet, ReviewViewSet
from .views import CommentViewSetAuthor, ReviewViewSet, TitleViewSet

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
)  # r'posts/(?P<post_id>\d+)/
api_router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Временно
    path('api/v1/', include(api_router_v1.urls)),

 ]
