from django.db import models

# Create your models here.
from django.db import models
from students.models import Student
from classes.models import AcademicTerm
from teachers.models import Teacher

class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reports')
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    overall_grade = models.CharField(max_length=5)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    teacher_remark = models.TextField(blank=True)
    headteacher_remark = models.TextField(blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'term')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} - {self.term}"

class ReportSubjectEntry(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(max_length=100)
    grade = models.CharField(max_length=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.report.student} - {self.subject_name}"
