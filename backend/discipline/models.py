from django.db import models
from django.conf import settings
from students.models import Student

class DisciplineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Discipline Categories"

    def __str__(self):
        return self.name

class DisciplinaryAction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DisciplineRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='discipline_records')
    category = models.ForeignKey(DisciplineCategory, on_delete=models.SET_NULL, null=True)
    action_taken = models.ForeignKey(DisciplinaryAction, on_delete=models.SET_NULL, null=True, blank=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_discipline_cases')
    date_reported = models.DateField(auto_now_add=True)
    incident_date = models.DateField()
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student} - {self.category} on {self.incident_date}"
