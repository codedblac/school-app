from django.db import models
from django.conf import settings
from students.models import Student
from academics.models import Subject, Term  # Change here from AcademicTerm to Term

class GradingScale(models.Model):
    name = models.CharField(max_length=100, unique=True)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-max_score']

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score})"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)  # Use Term here
    score = models.DecimalField(max_digits=6, decimal_places=2)
    grade_scale = models.ForeignKey(GradingScale, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comments = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'term')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.score}"

    def save(self, *args, **kwargs):
        # Automatically assign grading scale based on score
        if not self.grade_scale:
            scale = GradingScale.objects.filter(min_score__lte=self.score, max_score__gte=self.score).first()
            if scale:
                self.grade_scale = scale
        super().save(*args, **kwargs)
