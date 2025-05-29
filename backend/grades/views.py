from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from .models import Grade, GradingScale
from .serializers import GradeSerializer, GradingScaleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related(
        'student', 'subject', 'term', 'teacher', 'grade_scale'
    ).all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'subject', 'term', 'teacher', 'grade_scale']
    search_fields = ['comments']
    ordering_fields = ['timestamp', 'score']
    ordering = ['-timestamp']

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_grades(self, request):
        """Get grades recorded by the current user (teacher)"""
        queryset = self.queryset.filter(teacher=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class GradingScaleViewSet(viewsets.ModelViewSet):
    queryset = GradingScale.objects.all()
    serializer_class = GradingScaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['grade', 'description']
    ordering_fields = ['min_score', 'max_score', 'grade']
    ordering = ['min_score']
