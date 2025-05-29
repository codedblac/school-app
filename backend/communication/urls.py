from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet, ContactRestrictionViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'contact-restrictions', ContactRestrictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
