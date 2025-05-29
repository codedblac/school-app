from rest_framework import serializers
from .models import Announcement, UserWidgetPreference, ActivityLog

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'message', 'target_roles',
            'created_by', 'created_by_name', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_by_name', 'created_at']

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else "System"


class UserWidgetPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWidgetPreference
        fields = ['id', 'user', 'widget_name', 'visible', 'position']
        read_only_fields = ['user']


class ActivityLogSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'user_full_name', 'action', 'timestamp', 'metadata']
        read_only_fields = ['user', 'timestamp']

    def get_user_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "Unknown"
