from django.contrib import admin

# Register your models here.
# e_learning/admin.py

from django.contrib import admin
from .models import Course, Module, Lesson, Material, Enrollment, LessonProgress

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [LessonInline]
    ordering = ('course', 'order')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'duration')
    inlines = [MaterialInline]
    ordering = ('module', 'order')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'uploaded_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed', 'progress')
    list_filter = ('completed',)
    search_fields = ('student__username', 'course__title')

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed',)
