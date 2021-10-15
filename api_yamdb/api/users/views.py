import os
import json
import time
from random import choice
from http import HTTPStatus

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.vary import vary_on_cookie
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, BasePermission, AllowAny
from django.http import JsonResponse
from rest_framework import filters, viewsets

from api.users.models import User, UserCSRF
from .permissions import IsAdmin, AnyPost
from .serializers import UserSerializer, AuthSignup


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

class AuthSignupViewSet(viewsets.ViewSet):
    serializer_class = AuthSignup
    permission_classes = (AnyPost,)

class Test():
    def __init__(self, *args, **kwargs):
        self.username = kwargs['username']
        self.email = kwargs['email']

@csrf_exempt
@require_http_methods(["POST"])
def send_mail(request):
    body = request.body
    data = json.loads(body.decode('utf8').replace("'", '"'))
    if 'username' in data and 'email' in data:
        print(AuthSignup(Test(**data)).data)
        letters = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789'
        user = data['username']
        csrf, _ = UserCSRF.objects.get_or_create(username=user)
        csrf.token = ''.join([choice(letters) for _ in range(32)])
        csrf.date = int(time.time() + 5 * 60)
        csrf.save()
        send_mail(
            'Авторизация на YaMDB',
            f'ваш код для авторизации: {csrf.token}',
            'auth@yamdb.ru',
            [data['email']],
            fail_silently=False,
        )
        return JsonResponse({'Ответ':'На ваш адрес было отправлено письмо с кодом подтверждения'})
    return JsonResponse({'Error':'Error'})

def text_analize(request):
    text = '12345'
    csrf = get_object_or_404(UserCSRF, token=text)
    if csrf.date < int(time.time()):
        raise UserCSRF.DoesNotExist
    user = csrf.user


def user_csrf(request):
    letters = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789'
    user = request.user
    csrf, _ = UserCSRF.objects.get_or_create(user=user)
    csrf.token = ''.join([choice(letters) for _ in range(32)])
    csrf.date = int(time.time() + 5 * 60)
    csrf.save()
    context = {
        'author': user,
        'CSRF_token': csrf.token,
    }

    return JsonResponse('На ваш адрес было отправлено письмо с кодом подтверждения')
