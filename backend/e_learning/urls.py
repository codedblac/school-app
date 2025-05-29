# e_learning/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, MaterialViewSet, EnrollmentViewSet, LessonProgressViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')
router.register(r'lesson-progress', LessonProgressViewSet, basename='lessonprogress')

urlpatterns = [
    path('', include(router.urls)),
]
