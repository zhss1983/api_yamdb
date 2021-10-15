from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Даёт разрещение аутентифицированному
    пользователю с статусом админа.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role == 'a')

class AnyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
