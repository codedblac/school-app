from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'timestamp', 'content_object', 'description', 'ip_address']

    def get_content_object(self, obj):
        return str(obj.content_object) if obj.content_object else None
