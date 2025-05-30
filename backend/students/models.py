from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    
    # Standardize this field name for consistency with admin
    enrolled_date = models.DateField(auto_now_add=True)
    
    # Related parents (limited to users with role='parent')
    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='children',
        limit_choices_to={'role': 'parent'},
        blank=True
    )

    current_class = models.CharField(max_length=100, blank=True, null=True)
    stream = models.CharField(max_length=100, blank=True, null=True)

    # NEW fields below
    grade_level = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    @property
    def attendance_percentage(self):
        return None

    @property
    def latest_report(self):
        return None
