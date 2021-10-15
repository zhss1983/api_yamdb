from django.urls import path, include
from . import views

urlpatterns = [
#path('api/v1/auth/', include('api.users.urls')),
    #path('signup/', views.AuthSignupViewSet.as_view, name='send_mail'),
    path('signup/', views.send_mail, name='send_mail'),
#    path('user/<str:username>/<int:post_id>/edit/',
#         views.post_edit,
#         name='post_edit'),
]
