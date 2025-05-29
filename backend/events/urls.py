from rest_framework.routers import DefaultRouter
from .views import EventCategoryViewSet, EventViewSet, EventAttendeeViewSet

router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet)
router.register(r'events', EventViewSet)
router.register(r'attendees', EventAttendeeViewSet)

urlpatterns = router.urls
