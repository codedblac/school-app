from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]  # You can customize more granular permissions here
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['date', 'student__id', 'school_class__id', 'status']
    search_fields = ['notes', 'student__user__first_name', 'student__user__last_name']
    ordering_fields = ['date', 'student__user__last_name']

    def perform_create(self, serializer):
        # Automatically set the teacher marking the attendance from the logged in user if Teacher model is linked to user
        teacher = getattr(self.request.user, 'teacher_profile', None)  # example relation, adjust if needed
        serializer.save(marked_by=teacher)
    
    def get_queryset(self):
        # Limit records to the school or classes the user has access to (customize per your auth logic)
        user = self.request.user
        if user.is_superuser:
            return AttendanceRecord.objects.all()
        # Example: filter attendance records to classes the teacher is assigned to
        if hasattr(user, 'teacher_profile'):
            return AttendanceRecord.objects.filter(school_class__teachers=user.teacher_profile)
        # Add more filters for students or admins as needed
        return AttendanceRecord.objects.none()
