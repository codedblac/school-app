from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassRoomViewSet, SchoolClassViewSet, ClassStudentViewSet

router = DefaultRouter()
router.register(r'classrooms', ClassRoomViewSet, basename='classroom')
router.register(r'schoolclasses', SchoolClassViewSet, basename='schoolclass')
router.register(r'classstudents', ClassStudentViewSet, basename='classstudent')

urlpatterns = [
    path('', include(router.urls)),
]
