from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows full access to admin users.
    Read-only access is allowed for unauthenticated or non-admin users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only for admin users
        return request.user and request.user.is_staff


class IsReporterOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the reporter of a discipline record
    or admin users to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the reporter or admin
        return request.user and (obj.reported_by == request.user or request.user.is_staff)
