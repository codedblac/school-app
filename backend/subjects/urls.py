from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectCategoryViewSet, SubjectViewSet, ClassSubjectViewSet

router = DefaultRouter()
router.register('categories', SubjectCategoryViewSet)
router.register('subjects', SubjectViewSet)
router.register('class-subjects', ClassSubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
