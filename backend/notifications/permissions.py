from rest_framework import permissions

class IsRecipientOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only recipient can read/write the notification
        return obj.recipient == request.user
