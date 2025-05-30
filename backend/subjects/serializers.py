from rest_framework import serializers
from .models import SubjectCategory, Subject, ClassSubject
from teachers.models import Teacher



class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    category = SubjectCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SubjectCategory.objects.all(), source='category', write_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'is_cbc', 'category', 'category_id']


class ClassSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source='subject', write_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True, required=False)

    class Meta:
        model = ClassSubject
        fields = ['id', 'school_class', 'subject', 'subject_id', 'teacher_id']
