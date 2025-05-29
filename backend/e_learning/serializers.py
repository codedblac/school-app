# e_learning/serializers.py

from rest_framework import serializers
from .models import Course, Module, Lesson, Material, Enrollment, LessonProgress

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'file', 'uploaded_at']

class LessonSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'duration', 'materials']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'instructor', 'is_published', 'created_at', 'updated_at', 'modules']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'course_id', 'enrolled_at', 'completed', 'progress']
        read_only_fields = ['student', 'enrolled_at', 'progress', 'completed']

    def create(self, validated_data):
        student = self.context['request'].user
        validated_data['student'] = student
        return super().create(validated_data)

class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), write_only=True, source='lesson')

    class Meta:
        model = LessonProgress
        fields = ['id', 'enrollment', 'lesson', 'lesson_id', 'completed', 'completed_at']
        read_only_fields = ['completed_at']

    def update(self, instance, validated_data):
        if validated_data.get('completed', False) and not instance.completed:
            instance.completed_at = timezone.now()
        return super().update(instance, validated_data)
