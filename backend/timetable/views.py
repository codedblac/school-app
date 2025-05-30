from django.shortcuts import render

# Create your views here.
# timetable/views.py

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LessonPeriod, TimetableEntry
from .serializers import LessonPeriodSerializer, TimetableEntrySerializer
from .permissions import IsSchoolStaffOrReadOnly
from .permissions import IsTeacherOrAdmin


class LessonPeriodViewSet(viewsets.ModelViewSet):
    queryset = LessonPeriod.objects.all().order_by('start_time')
    serializer_class = LessonPeriodSerializer
    permission_classes = [permissions.IsAuthenticated, IsSchoolStaffOrReadOnly]

class TimetableEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsTeacherOrAdmin]
    queryset = TimetableEntry.objects.all().order_by('day_of_week', 'period__start_time')
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsSchoolStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['class_room', 'day_of_week', 'teacher', 'subject', 'is_active']
    search_fields = ['day_of_week', 'class_room__name', 'subject__name', 'teacher__first_name']
    ordering_fields = ['day_of_week', 'period__start_time', 'subject__name']

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
