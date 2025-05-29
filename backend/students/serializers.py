from rest_framework import serializers
from .models import Student
from accounts.serializers import CustomUserSerializer
from classes.models import Class, Stream  # Adjust as per your app structure
from reports.models import Report  # For latest report if needed
from reports.serializers import ReportSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    parents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUserSerializer.Meta.model.objects.filter(role='parent'), required=False
    )
    current_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    stream = serializers.PrimaryKeyRelatedField(queryset=Stream.objects.all(), allow_null=True, required=False)

    # Read-only fields
    attendance_percentage = serializers.FloatField(read_only=True)
    latest_report = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'admission_number', 'current_class', 'stream',
            'parents', 'attendance_percentage', 'latest_report',
            # add other fields you have in model here
        ]
        read_only_fields = ['attendance_percentage', 'latest_report']

    def get_latest_report(self, obj):
        report = Report.objects.filter(student=obj).order_by('-created_at').first()
        if report:
            return ReportSerializer(report).data
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        parents_data = validated_data.pop('parents', [])

        # Create user
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)

        # Create student
        student = Student.objects.create(user=user, **validated_data)

        # Link parents
        student.parents.set(parents_data)

        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        parents_data = validated_data.pop('parents', None)

        if user_data:
            CustomUserSerializer.update(CustomUserSerializer(), instance.user, user_data)
        
        if parents_data is not None:
            instance.parents.set(parents_data)

        return super().update(instance, validated_data)
