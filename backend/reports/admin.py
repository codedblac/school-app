from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Report, ReportSubjectEntry

class ReportSubjectEntryInline(admin.TabularInline):
    model = ReportSubjectEntry
    extra = 1
    fields = ('subject_name', 'grade', 'comment')
    readonly_fields = ()
    show_change_link = True

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'class_name', 'overall_grade', 'attendance_percentage', 'created_at', 'created_by')
    list_filter = ('term', 'class_name', 'created_by')
    search_fields = ('student__first_name', 'student__last_name', 'class_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [ReportSubjectEntryInline]

@admin.register(ReportSubjectEntry)
class ReportSubjectEntryAdmin(admin.ModelAdmin):
    list_display = ('report', 'subject_name', 'grade')
    search_fields = ('subject_name', 'report__student__first_name', 'report__student__last_name')
    ordering = ('subject_name',)
