from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet,
    GradingScaleViewSet,
    GradeAnalyticsView,
    GradeSummaryReportView
)

router = DefaultRouter()
router.register(r'grades', GradeViewSet, basename='grades')
router.register(r'grading-scale', GradingScaleViewSet, basename='grading-scale')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', GradeAnalyticsView.as_view(), name='grade-analytics'),
    path('summary-report/', GradeSummaryReportView.as_view(), name='grade-summary-report'),
]
