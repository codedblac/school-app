from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassRoom(models.Model):
    """
    Represents a physical classroom, e.g., Room A, Lab 1, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    location_description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=30)

    class Meta:
        verbose_name = "Classroom"
        verbose_name_plural = "Classrooms"
        ordering = ['name']

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    """
    Represents a class group for a given academic year and stream.
    """
    name = models.CharField(max_length=100)
    stream = models.CharField(max_length=50, blank=True, null=True)
    academic_year = models.ForeignKey(
        'academics.AcademicYear',
        on_delete=models.CASCADE,
        related_name='school_classes'
    )
    class_teacher = models.ForeignKey(
        'teachers.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes'
    )
    is_cbc = models.BooleanField(default=False, help_text="CBC = Competency-Based Curriculum")
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes',
        help_text="Physical room assigned to this class (optional)"
    )

    class Meta:
        verbose_name = "School Class"
        verbose_name_plural = "School Classes"
        unique_together = ('name', 'stream', 'academic_year')
        ordering = ['name', 'stream']

    def __str__(self):
        stream_part = f" - {self.stream}" if self.stream else ""
        return f"{self.name}{stream_part} ({'CBC' if self.is_cbc else 'Standard'})"


class ClassStudent(models.Model):
    """
    Links students to classes. Tracks enrollment history.
    """
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='class_enrollments'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='enrolled_students'
    )
    date_joined = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True, help_text="Is the student currently active in this class?")

    class Meta:
        verbose_name = "Class Student"
        verbose_name_plural = "Class Students"
        unique_together = ('student', 'school_class')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.student} in {self.school_class}"
