from rest_framework import serializers
from .models import Grade, GradingScale
from students.serializers import StudentSerializer
from academics.serializers import SubjectSerializer, AcademicTermSerializer
from accounts.serializers import UserSummarySerializer

class GradingScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingScale
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    term = AcademicTermSerializer(read_only=True)
    teacher = UserSummarySerializer(read_only=True)
    grade_scale = GradingScaleSerializer(read_only=True)

    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade._meta.get_field('student').related_model.objects.all(),
        source='student',
        write_only=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade._meta.get_field('subject').related_model.objects.all(),
        source='subject',
        write_only=True
    )
    term_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade._meta.get_field('term').related_model.objects.all(),
        source='term',
        write_only=True
    )

    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'subject', 'term', 'score', 'grade_scale', 'teacher',
            'comments', 'timestamp',
            'student_id', 'subject_id', 'term_id'
        ]
        read_only_fields = ['grade_scale', 'teacher', 'timestamp']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['teacher'] = request.user
        return super().create(validated_data)
