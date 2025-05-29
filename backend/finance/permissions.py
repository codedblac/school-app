from rest_framework import permissions

class IsFinanceAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and (request.user.is_staff or request.user.has_perm('finance.manage_payments'))
