from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CommentViewSetAuthor, ReviewViewSet

api_router_v1 = DefaultRouter()
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
api_router_v1.register(
    'comments',
    CommentViewSetAuthor,
    basename='comments'
)  # r'posts/(?P<post_id>\d+)/

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include(api_router_v1.urls)),
    # Getting token pair for user
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
