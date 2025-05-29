from rest_framework import serializers
from .models import (
    MedicalCondition, Medication, Doctor, MedicalRecord, MedicationLog,
    DoctorVisit, EmergencyContact, HealthScreening
)
from students.serializers import StudentSerializer  # assuming you have this

class MedicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCondition
        fields = ['id', 'name', 'description']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'description', 'instructions']

class DoctorSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'user_full_name', 'user_email', 'specialization', 'phone', 'email']

class MedicalRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=None, source='student', write_only=True)
    condition = MedicalConditionSerializer(read_only=True)
    condition_id = serializers.PrimaryKeyRelatedField(queryset=MedicalCondition.objects.all(), source='condition', write_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['id', 'student', 'student_id', 'condition', 'condition_id', 'diagnosed_on', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically assign Student queryset if context available
        if 'context' in kwargs and 'request' in kwargs['context']:
            self.fields['student_id'].queryset = self.context['request'].user.students.all() if hasattr(self.context['request'].user, 'students') else Student.objects.all()

class MedicationLogSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(read_only=True)
    medication_id = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), source='medication', write_only=True)

    class Meta:
        model = MedicationLog
        fields = ['id', 'record', 'medication', 'medication_id', 'start_date', 'end_date', 'dosage', 'instructions']

    def validate(self, data):
        if data.get('end_date') and data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be earlier than start date.")
        return data

class DoctorVisitSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=None, source='student', write_only=True)
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), source='doctor', write_only=True)

    class Meta:
        model = DoctorVisit
        fields = ['id', 'student', 'student_id', 'doctor', 'doctor_id', 'visit_date', 'reason', 'prescription', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs and 'request' in kwargs['context']:
            self.fields['student_id'].queryset = self.context['request'].user.students.all() if hasattr(self.context['request'].user, 'students') else Student.objects.all()

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'student', 'name', 'relation', 'phone', 'email']

class HealthScreeningSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=None, source='student', write_only=True)

    class Meta:
        model = HealthScreening
        fields = [
            'id', 'student', 'student_id', 'screening_date', 'height_cm', 'weight_kg',
            'vision_left', 'vision_right', 'hearing_test_passed', 'notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs and 'request' in kwargs['context']:
            self.fields['student_id'].queryset = self.context['request'].user.students.all() if hasattr(self.context['request'].user, 'students') else Student.objects.all()
