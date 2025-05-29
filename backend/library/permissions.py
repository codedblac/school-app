from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admin users.
    Read-only access to others.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to allow users to modify only their own bookmarks,
    but admins can manage all.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow if user is admin
        if request.user and request.user.is_staff:
            return True
        
        # Otherwise, only allow if the user owns the object
        return obj.user == request.user


class CanDownloadResource(permissions.BasePermission):
    """
    Controls access to download library items.
    For example, you can restrict downloads to authenticated users,
    or users with specific roles.
    """
    def has_permission(self, request, view):
        # Only authenticated users can download
        return request.user and request.user.is_authenticated
