from django.contrib import admin
from .models import ClassRoom, SchoolClass, ClassStudent

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_description', 'capacity')
    search_fields = ('name',)
    list_filter = ('capacity',)


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'academic_year', 'class_teacher', 'is_cbc', 'classroom')
    list_filter = ('academic_year', 'is_cbc')
    search_fields = ('name', 'stream', 'class_teacher__user__first_name', 'class_teacher__user__last_name')
    autocomplete_fields = ('academic_year', 'class_teacher', 'classroom')


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_class', 'date_joined', 'active')
    list_filter = ('active', 'school_class')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'school_class__name')
    autocomplete_fields = ('student', 'school_class')
    readonly_fields = ('date_joined',)
