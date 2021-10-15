from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, BasePermission, AllowAny
from django.contrib.auth.models import AnonymousUser


class EditAccessOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return (request.user and
                (obj.author == request.user or
            request.user.is_staff or
            request.user.role in ('moderator', 'admin'))
        )


class AdminOrReadOnly(BasePermission):
    """Object-level permission to only allow administrator."""

    def has_permission(self, request, view):
        a1 = request.method in SAFE_METHODS
        a2 = request.user and request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')
        rez = a1 or a2

        return rez



#    def has_object_permission(self, request, view, obj):
#        return request.user.is_staff or request.user.role == 'admin'


class GetPostDeleteMethod(BasePermission):

    def has_permission(self, request, view):
        return request.method in ('GET', 'POST', 'DELETE')

    def has_object_permission(self, request, view, obj):
        return request.method in ('GET', 'POST', 'DELETE')
