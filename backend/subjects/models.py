from django.db import models
from django.utils.translation import gettext_lazy as _
from teachers.models import Teacher
from classes.models import SchoolClass


class SubjectCategory(models.Model):
    """
    Categories like 'Languages', 'Sciences', 'Humanities', etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    A school subject, e.g., Mathematics, Biology.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(
        SubjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_cbc = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'code')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({'CBC' if self.is_cbc else 'Standard'})"


class ClassSubject(models.Model):
    """
    Links subjects to classes, optionally with an assigned teacher.
    """
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('school_class', 'subject')
        verbose_name = "Class Subject"
        verbose_name_plural = "Class Subjects"

    def __str__(self):
        return f"{self.subject.name} for {self.school_class}"
