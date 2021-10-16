from rest_framework.permissions import (BasePermission,
                                        IsAuthenticatedOrReadOnly,
                                        SAFE_METHODS)


class EditAccessOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        author = auth and obj.author == request.user
        admin = auth and (request.user.is_superuser or request.user.role in (
        'moderator', 'admin'))
        return safe or author or admin


class AdminOrReadOnly(BasePermission):
    """Object-level permission to only allow administrator."""

    def has_permission(self, request, view):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        admin = auth and (request.user.is_superuser or request.user.role == 'admin')
        return safe or admin

class AdminOrModeratorOrReadOnly(BasePermission):
    """Object-level permission to only allow administrator."""

    def has_permission(self, request, view):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        admin = auth and (request.user.is_superuser or request.user.role in (
        'moderator', 'admin'))
        return safe or admin
