from django.shortcuts import render

# Create your views here.
# e_learning/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Module, Lesson, Material, Enrollment, LessonProgress
from .serializers import (CourseSerializer, ModuleSerializer, LessonSerializer, MaterialSerializer, EnrollmentSerializer, LessonProgressSerializer)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Each user can see only their enrollments
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter to only progress records for enrollments belonging to user
        return LessonProgress.objects.filter(enrollment__student=self.request.user)

    def perform_create(self, serializer):
        # Ensure the enrollment belongs to the user
        enrollment = serializer.validated_data.get('enrollment')
        if enrollment.student != self.request.user:
            raise PermissionDenied("You cannot add progress to another user's enrollment")
        serializer.save()
