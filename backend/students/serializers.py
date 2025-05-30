from rest_framework import serializers
from .models import Student
from accounts.serializers import UserSerializer
from classes.models import SchoolClass
from reports.models import Report


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    parents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=UserSerializer.Meta.model.objects.filter(role='parent'),
        required=False
    )
    current_class = serializers.PrimaryKeyRelatedField(
        queryset=SchoolClass.objects.all()
    )
    stream = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    attendance_percentage = serializers.FloatField(read_only=True)
    latest_report = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'admission_number', 'current_class', 'stream',
            'parents', 'attendance_percentage', 'latest_report',
        ]
        read_only_fields = ['attendance_percentage', 'latest_report']

    def get_latest_report(self, obj):
        report = Report.objects.filter(student=obj).order_by('-created_at').first()
        if report:
            from reports.serializers import ReportSerializer  # Lazy import here
            return ReportSerializer(report).data
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        parents_data = validated_data.pop('parents', [])

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        student = Student.objects.create(user=user, **validated_data)

        student.parents.set(parents_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        parents_data = validated_data.pop('parents', None)

        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        if parents_data is not None:
            instance.parents.set(parents_data)

        return super().update(instance, validated_data)
