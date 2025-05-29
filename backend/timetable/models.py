from django.db import models

# Create your models here.
from django.db import models
from classes.models import ClassRoom  # Assuming a ClassRoom model exists
from subjects.models import Subject  # We'll create this app next if not done
from accounts.models import CustomUser

class LessonPeriod(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class TimetableEntry(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'}
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    period = models.ForeignKey(LessonPeriod, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, help_text="Optional notes or special instructions for the lesson.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('class_room', 'day_of_week', 'period')
        ordering = ['day_of_week', 'period__start_time']

    def __str__(self):
        return f"{self.class_room} | {self.subject} | {self.teacher} | {self.day_of_week} | {self.period}"

    def get_day_name(self):
        return dict(self.DAYS_OF_WEEK).get(self.day_of_week)
