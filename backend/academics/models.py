from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    teacher = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'teacher'}
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Term(models.Model):
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('academic_year', 'name')

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class Syllabus(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    class_level = models.ForeignKey('classes.SchoolClass', on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} - {self.topic}"

class LessonPlan(models.Model):
    syllabus = models.ForeignKey('Syllabus', on_delete=models.CASCADE)
    week = models.PositiveIntegerField()
    objective = models.TextField()
    activities = models.TextField()
    resources = models.TextField()
    assessment_method = models.TextField()

    def __str__(self):
        return f"Week {self.week} - {self.syllabus}"

class Assignment(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    class_level = models.ForeignKey('classes.SchoolClass', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.assignment}"
