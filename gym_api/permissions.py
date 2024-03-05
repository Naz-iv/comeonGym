from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to modify objects, but allow all users to view them.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (request.user
                and request.user.is_authenticated
                and request.user.is_staff)
