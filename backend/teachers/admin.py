from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'subject_specialization')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
