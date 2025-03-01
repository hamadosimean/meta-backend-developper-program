from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):
    """Only manager can create, delete or update, and other users have read permission."""

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_authenticated  # Corrected here
        return (
            request.user.groups.filter(name="Manager").exists()
            or request.user.is_superuser
        )


class OnlyManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name="Manager").exists()
            or request.user.is_superuser
        )
