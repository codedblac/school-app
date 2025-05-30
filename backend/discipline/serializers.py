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
    # Read-only nested representations
    student = serializers.StringRelatedField(read_only=True)
    category = DisciplineCategorySerializer(read_only=True)
    action_taken = DisciplinaryActionSerializer(read_only=True)
    reported_by = serializers.StringRelatedField(read_only=True)

    # Write-only PK fields
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=None,  # will be set dynamically in __init__
        source='student',
        write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DisciplineCategory.objects.all(),
        source='category',
        write_only=True
    )
    action_taken_id = serializers.PrimaryKeyRelatedField(
        queryset=DisciplinaryAction.objects.all(),
        source='action_taken',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = DisciplineRecord
        fields = [
            'id',
            'student', 'student_id',
            'category', 'category_id',
            'action_taken', 'action_taken_id',
            'reported_by',
            'incident_date', 'description',
            'is_resolved', 'resolution_notes',
            'date_reported', 'timestamp'
        ]
        read_only_fields = [
            'student', 'category', 'action_taken', 'reported_by',
            'date_reported', 'timestamp'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set Student queryset dynamically to avoid circular imports
        from students.models import Student
        self.fields['student_id'].queryset = Student.objects.all()

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['reported_by'] = request.user
        return super().create(validated_data)
