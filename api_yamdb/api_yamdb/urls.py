from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from api.users.views import MyTokenObtainPairView, UserViewSet
from .views import CommentViewSet, ReviewViewSet, TitleViewSet

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
    path('api/v1/auth/', include('api.users.urls')),
#    path('/signup/', views.post_edit, name='post_edit')
#    path('user/<str:username>/<int:post_id>/edit/',
#         views.post_edit,
#         name='post_edit'),
    path('api/v1/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Временно
    path('api/v1/', include(api_router_v1.urls)),
 ]
