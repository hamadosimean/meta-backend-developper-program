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


class IsManagerOrAdmin(permissions.BasePermission):
    """Manager permission"""

    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name="Manager").exists()
            or request.user.is_superuser
        )


class IsOwner(permissions.BasePermission):
    """Object created by a particular user can be edited by this particular user"""

    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        # Allow read access to all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only to the owner of the object
        return request.user == obj.user
