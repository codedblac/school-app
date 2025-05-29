# timetable/permissions.py

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access to admin users.
    Read-only access for others.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser

class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Allow access only to teachers assigned or admins.
    """

    def has_permission(self, request, view):
        # Allow admins full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Allow teachers (assuming role='teacher' in user model)
        return getattr(request.user, 'role', None) == 'teacher'

    def has_object_permission(self, request, view, obj):
        # Admins get full access
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Teachers can only access timetable entries assigned to them
        return obj.teacher == request.user

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Students have read-only access.
    Admins and teachers can modify.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admin or teacher can write
        return request.user.is_staff or getattr(request.user, 'role', None) == 'teacher'
