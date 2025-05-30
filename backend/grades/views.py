from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Count

from .models import Grade, GradingScale
from .serializers import GradeSerializer, GradingScaleSerializer

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


class GradeAnalyticsView(APIView):
    """
    Basic analytics on grade data across the system.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "average_score": Grade.objects.aggregate(avg=Avg('score'))['avg'],
            "max_score": Grade.objects.aggregate(max=Max('score'))['max'],
            "min_score": Grade.objects.aggregate(min=Min('score'))['min'],
            "grades_count": Grade.objects.count(),
            "grades_per_subject": Grade.objects.values('subject__name').annotate(total=Count('id')),
            "grades_per_teacher": Grade.objects.values('teacher__email').annotate(total=Count('id')),
        }
        return Response(data, status=status.HTTP_200_OK)


class GradeSummaryReportView(APIView):
    """
    Summary report: average grade per student and per subject.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        summary = {
            "average_per_student": Grade.objects.values('student__id', 'student__user__first_name', 'student__user__last_name')
                .annotate(average_score=Avg('score'))
                .order_by('-average_score'),

            "average_per_subject": Grade.objects.values('subject__id', 'subject__name')
                .annotate(average_score=Avg('score'))
                .order_by('-average_score'),
        }
        return Response(summary, status=status.HTTP_200_OK)
