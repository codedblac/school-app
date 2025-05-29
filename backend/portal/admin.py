from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Announcement, UserWidgetPreference, ActivityLog

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('target_roles', 'created_at')
    search_fields = ('title', 'message', 'created_by__username')
    autocomplete_fields = ['created_by']
    filter_horizontal = ('target_roles',)
    readonly_fields = ('created_at',)

@admin.register(UserWidgetPreference)
class UserWidgetPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'widget_name', 'visible', 'position')
    list_filter = ('visible',)
    search_fields = ('user__username', 'widget_name')
    autocomplete_fields = ['user']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'action', 'metadata')
    autocomplete_fields = ['user']
    readonly_fields = ('timestamp',)
