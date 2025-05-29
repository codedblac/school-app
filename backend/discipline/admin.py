from django.contrib import admin
from .models import DisciplineCategory, DisciplinaryAction, DisciplineRecord

@admin.register(DisciplineCategory)
class DisciplineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(DisciplinaryAction)
class DisciplinaryActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(DisciplineRecord)
class DisciplineRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'action_taken', 'reported_by', 'incident_date', 'is_resolved', 'timestamp')
    list_filter = ('category', 'action_taken', 'is_resolved', 'incident_date')
    search_fields = ('student__first_name', 'student__last_name', 'description', 'resolution_notes')
    readonly_fields = ('date_reported', 'timestamp')
    date_hierarchy = 'incident_date'
    ordering = ('-timestamp',)

    fieldsets = (
        (None, {
            'fields': ('student', 'category', 'action_taken', 'reported_by', 'incident_date', 'description')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolution_notes'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('date_reported', 'timestamp'),
        }),
    )
