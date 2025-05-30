from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'admission_number',
        'grade_level',
        'stream',
        'gender',
        'date_of_birth',
        'is_active',
        'enrolled_date',
    )
    list_filter = (
        'grade_level',
        'stream',
        'gender',
        'is_active',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'admission_number',
    )
    ordering = ('-enrolled_date',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'enrolled_date'

    autocomplete_fields = ('user',)  
