from django.contrib import admin

from django.contrib import admin
from .models import SchoolAnalytics

@admin.register(SchoolAnalytics)
class SchoolAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('school', 'total_students', 'total_teachers', 'average_attendance_rate', 'average_performance', 'last_updated')
    readonly_fields = ('last_updated',)

