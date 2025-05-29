from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisciplineCategoryViewSet, DisciplinaryActionViewSet, DisciplineRecordViewSet

router = DefaultRouter()
router.register(r'categories', DisciplineCategoryViewSet, basename='disciplinecategory')
router.register(r'actions', DisciplinaryActionViewSet, basename='disciplinaryaction')
router.register(r'records', DisciplineRecordViewSet, basename='disciplinerecord')

urlpatterns = [
    path('', include(router.urls)),
]
