from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS, BasePermission

class IsModerator(BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.role in 'M'


class IsAdmin(BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.role == 'A'


class IsAuthor(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAuthorOrModeratorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (
                obj.author == request.user or
                request.user.is_staff or
                request.user.role in 'MA'
            )
        )
