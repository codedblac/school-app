from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admins, read-only for others.
    """

    def has_permission(self, request, view):
        # Safe methods (GET, HEAD, OPTIONS) allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for admin users
        return request.user and request.user.is_staff

class IsReporterOrAdmin(permissions.BasePermission):
    """
    Allow the reporter of a discipline record or an admin to edit/delete.
    Others can only read.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions for the reporter or admin
        return obj.reported_by == request.user or request.user.is_staff
