from rest_framework import serializers
from .models import ClassRoom, SchoolClass, ClassStudent
from students.serializers import StudentSerializer  # Assuming you have this
from teachers.serializers import TeacherSerializer  # Assuming you have this
from academics.serializers import AcademicYearSerializer  # Assuming you have this

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'name', 'location_description', 'capacity']


class SchoolClassSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicYearSerializer.Meta.model.objects.all(), source='academic_year', write_only=True
    )
    class_teacher = TeacherSerializer(read_only=True)
    class_teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=TeacherSerializer.Meta.model.objects.all(), source='class_teacher', write_only=True, allow_null=True, required=False
    )
    classroom = ClassRoomSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassRoom.objects.all(), source='classroom', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = SchoolClass
        fields = [
            'id',
            'name',
            'stream',
            'academic_year',
            'academic_year_id',
            'class_teacher',
            'class_teacher_id',
            'is_cbc',
            'classroom',
            'classroom_id',
        ]


class ClassStudentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentSerializer.Meta.model.objects.all(), source='student', write_only=True
    )
    school_class = SchoolClassSerializer(read_only=True)
    school_class_id = serializers.PrimaryKeyRelatedField(
        queryset=SchoolClass.objects.all(), source='school_class', write_only=True
    )

    class Meta:
        model = ClassStudent
        fields = [
            'id',
            'student',
            'student_id',
            'school_class',
            'school_class_id',
            'date_joined',
            'active',
        ]
        read_only_fields = ['date_joined']
