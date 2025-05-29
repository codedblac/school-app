from rest_framework import viewsets, permissions
from .models import ClassRoom, SchoolClass, ClassStudent
from .serializers import ClassRoomSerializer, SchoolClassSerializer, ClassStudentSerializer

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [permissions.IsAuthenticated]  # Customize permissions as needed


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.select_related(
        'academic_year', 'class_teacher', 'classroom'
    ).all()
    serializer_class = SchoolClassSerializer
    permission_classes = [permissions.IsAuthenticated]  # Customize permissions as needed


class ClassStudentViewSet(viewsets.ModelViewSet):
    queryset = ClassStudent.objects.select_related(
        'student', 'school_class'
    ).all()
    serializer_class = ClassStudentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Customize permissions as needed
