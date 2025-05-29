from django.contrib import admin

# academics/admin.py

from django.contrib import admin
from .models import Subject, AcademicYear, Term, Syllabus, LessonPlan, Assignment, Submission

admin.site.register(Subject)
admin.site.register(AcademicYear)
admin.site.register(Term)
admin.site.register(Syllabus)
admin.site.register(LessonPlan)
admin.site.register(Assignment)
admin.site.register(Submission)
