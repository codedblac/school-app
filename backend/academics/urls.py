# academics/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, AcademicYearViewSet, TermViewSet,
    SyllabusViewSet, LessonPlanViewSet, AssignmentViewSet, SubmissionViewSet
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'terms', TermViewSet)
router.register(r'syllabuses', SyllabusViewSet)
router.register(r'lesson-plans', LessonPlanViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
