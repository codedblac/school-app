from django.contrib import admin
from .models import (
    Subject, AcademicYear, AcademicTerm,
    Syllabus, LessonPlan, Assignment, Submission
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    search_fields = (
        'name', 'code',
        'teacher__user__first_name', 'teacher__user__last_name',
        'teacher__employee_id'
    )
    autocomplete_fields = ('teacher',)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'academic_year')
    search_fields = ('name', 'academic_year__name')
    list_filter = ('academic_year',)
    autocomplete_fields = ('academic_year',)


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('subject', 'academic_term', 'title')
    search_fields = ('title', 'subject__name', 'academic_term__name')
    list_filter = ('subject', 'academic_term')
    autocomplete_fields = ('subject', 'academic_term')


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('syllabus', 'topic', 'created_at')
    search_fields = ('topic', 'syllabus__title', 'syllabus__subject__name')
    list_filter = ('created_at',)
    autocomplete_fields = ('syllabus',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'due_date')
    search_fields = ('title', 'subject__name')
    list_filter = ('due_date',)
    autocomplete_fields = ('subject',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'graded')
    search_fields = (
        'assignment__title',
        'student__user__first_name', 'student__user__last_name'
    )
    list_filter = ('graded',)
    autocomplete_fields = ('assignment', 'student')
