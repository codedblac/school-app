from rest_framework import serializers
from .models import LibraryCategory, LibraryItem, BookmarkedItem, DownloadLog, ViewLog
from django.contrib.auth import get_user_model

User = get_user_model()

class LibraryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryCategory
        fields = ['id', 'name', 'description']

class LibraryItemSerializer(serializers.ModelSerializer):
    category = LibraryCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=LibraryCategory.objects.all(), source='category', write_only=True
    )
    uploaded_by = serializers.StringRelatedField(read_only=True)
    download_count = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    virus_scan_status = serializers.CharField(read_only=True)
    virus_scan_report = serializers.CharField(read_only=True)

    class Meta:
        model = LibraryItem
        fields = [
            'id', 'title', 'category', 'category_id', 'resource_type', 'description',
            'preview_text', 'file', 'thumbnail', 'uploaded_by', 'upload_date', 'download_count',
            'view_count', 'virus_scan_status', 'virus_scan_report', 'is_active',
        ]
        read_only_fields = ['upload_date', 'uploaded_by', 'download_count', 'view_count', 'virus_scan_status', 'virus_scan_report']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['uploaded_by'] = user
        return super().create(validated_data)

class BookmarkedItemSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    item = LibraryItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=LibraryItem.objects.filter(is_active=True), source='item', write_only=True
    )

    class Meta:
        model = BookmarkedItem
        fields = ['id', 'user', 'item', 'item_id', 'bookmarked_at']
        read_only_fields = ['user', 'bookmarked_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class DownloadLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    item = LibraryItemSerializer(read_only=True)

    class Meta:
        model = DownloadLog
        fields = ['id', 'user', 'item', 'download_date', 'ip_address']

class ViewLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    item = LibraryItemSerializer(read_only=True)

    class Meta:
        model = ViewLog
        fields = ['id', 'user', 'item', 'view_date', 'ip_address']
