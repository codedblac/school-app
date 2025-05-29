from rest_framework import serializers
from .models import DisciplineCategory, DisciplinaryAction, DisciplineRecord

class DisciplineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplineCategory
        fields = ['id', 'name', 'description']

class DisciplinaryActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisciplinaryAction
        fields = ['id', 'name', 'description']

class DisciplineRecordSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    category = DisciplineCategorySerializer(read_only=True)
    action_taken = DisciplinaryActionSerializer(read_only=True)
    reported_by = serializers.StringRelatedField(read_only=True)

    # Allow write by pk for foreign keys
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DisciplineCategory.objects.all(), source='category', write_only=True
    )
    action_taken_id = serializers.PrimaryKeyRelatedField(
        queryset=DisciplinaryAction.objects.all(), source='action_taken', write_only=True, allow_null=True, required=False
    )
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=None, source='student', write_only=True
    )

    class Meta:
        model = DisciplineRecord
        fields = [
            'id', 'student', 'student_id', 'category', 'category_id', 'action_taken', 'action_taken_id',
            'reported_by', 'date_reported', 'incident_date', 'description', 'is_resolved',
            'resolution_notes', 'timestamp'
        ]
        read_only_fields = ['date_reported', 'reported_by', 'timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We must set student queryset dynamically because Student model might be dynamic or filtered by school
        from students.models import Student
        self.fields['student_id'].queryset = Student.objects.all()

    def create(self, validated_data):
        # set reported_by from context (request.user)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['reported_by'] = request.user
        return super().create(validated_data)
