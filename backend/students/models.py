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
    enrollment_date = models.DateField(auto_now_add=True)

    # Link to parents - ManyToMany since a student can have multiple parents/guardians
    parents = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='children',
        limit_choices_to={'role': 'parent'},
        blank=True
    )

    current_class = models.CharField(max_length=100, blank=True, null=True)
    stream = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    @property
    def attendance_percentage(self):
        # Replace with actual attendance logic
        return None

    @property
    def latest_report(self):
        # Replace with actual report fetching logic
        return None
