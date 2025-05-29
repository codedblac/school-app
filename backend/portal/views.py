from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.db.models import Q
from .models import Announcement, UserWidgetPreference, ActivityLog
from .serializers import AnnouncementSerializer, UserWidgetPreferenceSerializer, ActivityLogSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        user = self.request.user
        roles = user.roles if hasattr(user, 'roles') else []
        query = Q(target_roles__overlap=roles) | Q(target_roles__contains=["all"])
        return Announcement.objects.filter(query).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserWidgetPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserWidgetPreference.objects.all()
    serializer_class = UserWidgetPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-timestamp')
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
