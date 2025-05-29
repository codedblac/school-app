from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, UserWidgetPreferenceViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'widget-preferences', UserWidgetPreferenceViewSet, basename='widgetpreference')
router.register(r'activity-logs', ActivityLogViewSet, basename='activitylog')

urlpatterns = [
    path('', include(router.urls)),
]
