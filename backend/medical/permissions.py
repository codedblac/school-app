# medical/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """
    Allow read-only access to everyone, but write access to staff only.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrStaff(BasePermission):
    """
    Allow access to the object's owner or staff members.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.student.user == request.user
