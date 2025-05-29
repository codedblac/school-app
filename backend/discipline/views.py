from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DisciplineCategory, DisciplinaryAction, DisciplineRecord
from .serializers import (
    DisciplineCategorySerializer,
    DisciplinaryActionSerializer,
    DisciplineRecordSerializer,
)
from .permissions import IsAdminOrReadOnly, IsReporterOrAdmin

class DisciplineCategoryViewSet(viewsets.ModelViewSet):
    queryset = DisciplineCategory.objects.all()
    serializer_class = DisciplineCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admins can create/update/delete

class DisciplinaryActionViewSet(viewsets.ModelViewSet):
    queryset = DisciplinaryAction.objects.all()
    serializer_class = DisciplinaryActionSerializer
    permission_classes = [IsAdminOrReadOnly]

class DisciplineRecordViewSet(viewsets.ModelViewSet):
    queryset = DisciplineRecord.objects.select_related(
        'student', 'category', 'action_taken', 'reported_by'
    ).all()
    serializer_class = DisciplineRecordSerializer
    permission_classes = [IsReporterOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'category', 'is_resolved', 'incident_date']
    search_fields = ['description', 'resolution_notes', 'student__first_name', 'student__last_name']
    ordering_fields = ['date_reported', 'incident_date', 'timestamp']
    ordering = ['-timestamp']

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
