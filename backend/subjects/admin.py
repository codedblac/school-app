from django.contrib import admin
from .models import SubjectCategory, Subject, ClassSubject


@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'is_cbc')
    list_filter = ('is_cbc', 'category')
    search_fields = ('name', 'code')


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'school_class', 'teacher')
    list_filter = ('school_class', 'teacher')
    search_fields = ('subject__name', 'school_class__name')
