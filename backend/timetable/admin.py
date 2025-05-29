from django.contrib import admin

# Register your models here.
# timetable/admin.py

from django.contrib import admin
from .models import LessonPeriod, TimetableEntry

@admin.register(LessonPeriod)
class LessonPeriodAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')
    ordering = ('start_time',)
    search_fields = ('start_time', 'end_time')

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('class_room', 'subject', 'teacher', 'day_of_week', 'period', 'is_active')
    list_filter = ('day_of_week', 'class_room', 'subject', 'teacher', 'is_active')
    search_fields = ('class_room__name', 'subject__name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('day_of_week', 'period__start_time')

    autocomplete_fields = ('class_room', 'subject', 'teacher', 'period')

    def get_readonly_fields(self, request, obj=None):
        # Example: Only superusers can edit is_active status
        if not request.user.is_superuser:
            return ['is_active']
        return []
