from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalConditionViewSet,
    MedicationViewSet,
    DoctorViewSet,
    MedicalRecordViewSet,
    MedicationLogViewSet,
    DoctorVisitViewSet,
    EmergencyContactViewSet,
    HealthScreeningViewSet,
)

router = DefaultRouter()
router.register(r'medical-conditions', MedicalConditionViewSet, basename='medicalcondition')
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'medical-records', MedicalRecordViewSet, basename='medicalrecord')
router.register(r'medication-logs', MedicationLogViewSet, basename='medicationlog')
router.register(r'doctor-visits', DoctorVisitViewSet, basename='doctorvisit')
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergencycontact')
router.register(r'health-screenings', HealthScreeningViewSet, basename='healthscreening')

urlpatterns = [
    path('', include(router.urls)),
]
