from django.contrib import admin
from .models import (
    MedicalCondition, Medication, Doctor, MedicalRecord, MedicationLog,
    DoctorVisit, EmergencyContact, HealthScreening
)

@admin.register(MedicalCondition)
class MedicalConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'phone', 'email')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialization', 'phone', 'email')
    list_filter = ('specialization',)

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'condition', 'is_resolved', 'date_reported', 'incident_date')
    list_filter = ('condition', 'is_resolved', 'date_reported')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'condition__name', 'notes')
    date_hierarchy = 'date_reported'
    ordering = ('-date_reported',)

@admin.register(MedicationLog)
class MedicationLogAdmin(admin.ModelAdmin):
    list_display = ('record', 'medication', 'dosage', 'start_date', 'end_date')
    list_filter = ('medication', 'start_date', 'end_date')
    search_fields = ('record__student__user__first_name', 'record__student__user__last_name', 'medication__name')
    ordering = ('-start_date',)

@admin.register(DoctorVisit)
class DoctorVisitAdmin(admin.ModelAdmin):
    list_display = ('student', 'doctor', 'visit_date', 'reason')
    list_filter = ('doctor', 'visit_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'doctor__user__username', 'reason')
    ordering = ('-visit_date',)

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('student', 'name', 'relation', 'phone')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'name', 'relation', 'phone')
    list_filter = ('relation',)

@admin.register(HealthScreening)
class HealthScreeningAdmin(admin.ModelAdmin):
    list_display = ('student', 'screening_date', 'notes')
    list_filter = ('screening_date',)
    search_fields = ('student__user__first_name', 'student__user__last_name', 'notes')
    ordering = ('-screening_date',)
