from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admin users.
    Read-only access to others.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsReportOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a report or admins to edit it.
    Others can only read if permitted.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions allowed to any user
        if request.method in permissions.SAFE_METHODS:
            # Optionally, add more checks if reports are sensitive
            return True
        
        # Write permissions only to the owner or admin
        return obj.owner == request.user or request.user.is_staff


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Allow access only to teachers or admin users.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.role == 'teacher')


class IsParentOrAdmin(permissions.BasePermission):
    """
    Allow access only to parents or admin users.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.role == 'parent')

