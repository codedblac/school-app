from django.db import models
from django.conf import settings
from students.models import Student

class MedicalCondition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

class MedicalRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.ForeignKey(MedicalCondition, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosed_on = models.DateField(null=True, blank=True)

    # 🆕 Fields added for admin compatibility
    incident_date = models.DateField(null=True, blank=True)
    date_reported = models.DateField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.condition}"

    class Meta:
        ordering = ['-date_reported']

class MedicationLog(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='medications')
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication} for {self.record.student}"

class DoctorVisit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='doctor_visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    reason = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit: {self.student} with Dr. {self.doctor} on {self.visit_date}"

class EmergencyContact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.relation}) for {self.student}"

class HealthScreening(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='health_screenings')
    screening_date = models.DateField()
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    vision_left = models.CharField(max_length=10, blank=True)
    vision_right = models.CharField(max_length=10, blank=True)
    hearing_test_passed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Health Screening: {self.student} on {self.screening_date}"
