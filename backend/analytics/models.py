from django.db import models
from django.conf import settings

class SubjectPerformance(models.Model):
    analytics = models.ForeignKey('SchoolAnalytics', on_delete=models.CASCADE, related_name='subject_performances')
    subject_name = models.CharField(max_length=100)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.subject_name} Performance: {self.average_score}"

class AttendanceTrend(models.Model):
    analytics = models.ForeignKey('SchoolAnalytics', on_delete=models.CASCADE, related_name='attendance_trends')
    month = models.DateField(help_text="First day of the month")
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Attendance {self.month.strftime('%b %Y')}: {self.attendance_rate}"

class DisciplineRecordSummary(models.Model):
    analytics = models.ForeignKey('SchoolAnalytics', on_delete=models.CASCADE, related_name='discipline_summaries')
    month = models.DateField(help_text="First day of the month")
    incidents_reported = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Discipline incidents in {self.month.strftime('%b %Y')}: {self.incidents_reported}"

class SchoolAnalytics(models.Model):
    school = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    total_students = models.PositiveIntegerField(default=0)
    total_teachers = models.PositiveIntegerField(default=0)
    average_attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    average_performance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.school}"
