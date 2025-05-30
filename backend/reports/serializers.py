from rest_framework import serializers
from .models import Report, ReportSubjectEntry
from students.models import Student  # ✅ Import the model directly

class ReportSubjectEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSubjectEntry
        fields = ['id', 'subject_name', 'grade', 'comment']

class ReportSerializer(serializers.ModelSerializer):
    subject_entries = ReportSubjectEntrySerializer(many=True, required=False)
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all()  # ✅ Provide valid queryset
    )

    class Meta:
        model = Report
        fields = [
            'id', 'student', 'term', 'class_name', 'overall_grade',
            'attendance_percentage', 'created_at', 'created_by',
            'subject_entries',
        ]
        read_only_fields = ['created_at', 'created_by']

    def create(self, validated_data):
        subject_entries_data = validated_data.pop('subject_entries', [])
        report = Report.objects.create(**validated_data)
        for entry_data in subject_entries_data:
            ReportSubjectEntry.objects.create(report=report, **entry_data)
        return report

    def update(self, instance, validated_data):
        subject_entries_data = validated_data.pop('subject_entries', [])
        instance.term = validated_data.get('term', instance.term)
        instance.class_name = validated_data.get('class_name', instance.class_name)
        instance.overall_grade = validated_data.get('overall_grade', instance.overall_grade)
        instance.attendance_percentage = validated_data.get('attendance_percentage', instance.attendance_percentage)
        instance.save()

        instance.subject_entries.all().delete()
        for entry_data in subject_entries_data:
            ReportSubjectEntry.objects.create(report=instance, **entry_data)

        return instance
