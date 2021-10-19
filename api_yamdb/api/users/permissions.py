from rest_framework import permissions

from .models import ADMIN_LEVEL

class IsAdmin(permissions.BasePermission):
    """Даёт разрещение аутентифицированному пользователю с статусом админа."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and ((request.user.role == ADMIN_LEVEL)
                     or request.user.is_superuser))
