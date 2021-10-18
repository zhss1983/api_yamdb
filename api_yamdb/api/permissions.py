from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class EditAccessOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow access level users (author,
    moderator, administrator) to edit it.
    Assumes the model instance has an `author` attribute.
    """
    FULL_ACCESS = ('moderator', 'admin')

    def has_object_permission(self, request, view, obj):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        author = auth and obj.author == request.user
        admin = auth and (
            request.user.is_superuser or request.user.role in self.FULL_ACCESS)
        return safe or author or admin


class AdminOrReadOnly(BasePermission):
    """
    Object-level permission to only allow access level users (author,
    administrator) to edit it.
    """

    def has_permission(self, request, view):
        safe = request.method in SAFE_METHODS
        auth = request.user and request.user.is_authenticated
        admin = auth and (request.user.is_superuser
                          or request.user.role == 'admin')
        return safe or admin
