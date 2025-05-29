from rest_framework import serializers
from .models import SchoolAnalytics, SubjectPerformance, AttendanceTrend, DisciplineRecordSummary

class SubjectPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectPerformance
        fields = ['subject_name', 'average_score']

class AttendanceTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceTrend
        fields = ['month', 'attendance_rate']

class DisciplineRecordSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineRecordSummary
        fields = ['month', 'incidents_reported']

class SchoolAnalyticsSerializer(serializers.ModelSerializer):
    subject_performances = SubjectPerformanceSerializer(many=True, read_only=True)
    attendance_trends = AttendanceTrendSerializer(many=True, read_only=True)
    discipline_summaries = DisciplineRecordSummarySerializer(many=True, read_only=True)

    class Meta:
        model = SchoolAnalytics
        fields = [
            'total_students',
            'total_teachers',
            'average_attendance_rate',
            'average_performance',
            'last_updated',
            'subject_performances',
            'attendance_trends',
            'discipline_summaries',
        ]
        read_only_fields = ('last_updated',)
