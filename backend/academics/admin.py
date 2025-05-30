from django.contrib import admin

# academics/admin.py

from django.contrib import admin
from .models import Subject, AcademicYear, AcademicTerm, Syllabus, LessonPlan, Assignment, Submission

admin.site.register(Subject)
admin.site.register(AcademicYear)
admin.site.register(AcademicTerm)
admin.site.register(Syllabus)
admin.site.register(LessonPlan)
admin.site.register(Assignment)
admin.site.register(Submission)
