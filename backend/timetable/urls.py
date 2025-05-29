# timetable/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LessonPeriodViewSet, TimetableEntryViewSet

router = DefaultRouter()
router.register(r'lesson-periods', LessonPeriodViewSet, basename='lessonperiod')
router.register(r'timetable-entries', TimetableEntryViewSet, basename='timetableentry')

urlpatterns = [
    path('', include(router.urls)),
]
