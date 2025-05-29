
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIInteractionLogViewSet

router = DefaultRouter()
router.register(r'interactions', AIInteractionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
