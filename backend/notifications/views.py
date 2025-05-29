from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'expire_at']
    search_fields = ['title', 'message']

    def get_queryset(self):
        # Each user sees only their own notifications
        return Notification.objects.filter(recipient=self.request.user)

    def perform_create(self, serializer):
        # Usually notifications created by system/admin, but can be extended
        serializer.save(recipient=self.request.user)
