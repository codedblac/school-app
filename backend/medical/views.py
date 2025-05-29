from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    MedicalCondition, Medication, Doctor, MedicalRecord, MedicationLog,
    DoctorVisit, EmergencyContact, HealthScreening
)
from .serializers import (
    MedicalConditionSerializer, MedicationSerializer, DoctorSerializer,
    MedicalRecordSerializer, MedicationLogSerializer, DoctorVisitSerializer,
    EmergencyContactSerializer, HealthScreeningSerializer
)
from .permissions import IsStaffOrReadOnly, IsOwnerOrStaff  # We'll create these later or you can adapt

class MedicalConditionViewSet(viewsets.ModelViewSet):
    queryset = MedicalCondition.objects.all()
    serializer_class = MedicalConditionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'condition', 'is_resolved']
    search_fields = ['description', 'resolution_notes']
    ordering_fields = ['date_reported', 'incident_date']

    def get_queryset(self):
        user = self.request.user
        # Adjust this logic based on your user/student relation
        if user.is_staff:
            return MedicalRecord.objects.all()
        # If user has linked students, filter by those students
        return MedicalRecord.objects.filter(student__in=user.students.all())

class MedicationLogViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['record', 'medication']
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicationLog.objects.all()
        return MedicationLog.objects.filter(record__student__in=user.students.all())

class DoctorVisitViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorVisitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'doctor', 'visit_date']
    search_fields = ['reason', 'notes']
    ordering_fields = ['visit_date']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return DoctorVisit.objects.all()
        return DoctorVisit.objects.filter(student__in=user.students.all())

class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student']
    search_fields = ['name', 'relation', 'phone']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return EmergencyContact.objects.all()
        return EmergencyContact.objects.filter(student__in=user.students.all())

class HealthScreeningViewSet(viewsets.ModelViewSet):
    serializer_class = HealthScreeningSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'screening_date']
    ordering_fields = ['screening_date']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return HealthScreening.objects.all()
        return HealthScreening.objects.filter(student__in=user.students.all())
