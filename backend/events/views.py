from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EventCategory, Event, EventAttendee
from .serializers import EventCategorySerializer, EventSerializer, EventAttendeeSerializer

class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__id', 'organizer']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_datetime', 'end_datetime', 'created_at']

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventAttendeeViewSet(viewsets.ModelViewSet):
    queryset = EventAttendee.objects.all()
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own RSVPs or events they organize
        user = self.request.user
        return self.queryset.filter(user=user) | self.queryset.filter(event__organizer=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
