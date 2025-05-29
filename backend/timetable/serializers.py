# timetable/serializers.py

from rest_framework import serializers
from .models import LessonPeriod, TimetableEntry
from classes.models import ClassRoom
from subjects.models import Subject
from accounts.models import CustomUser

class LessonPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPeriod
        fields = ['id', 'start_time', 'end_time']

class TimetableEntrySerializer(serializers.ModelSerializer):
    class_room = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ClassRoom.objects.all()
    )
    subject = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Subject.objects.all()
    )
    teacher = serializers.SlugRelatedField(
        slug_field='full_name',  # assuming CustomUser has full_name property/method
        queryset=CustomUser.objects.filter(role='teacher')
    )
    period = LessonPeriodSerializer()

    class Meta:
        model = TimetableEntry
        fields = [
            'id',
            'class_room',
            'subject',
            'teacher',
            'day_of_week',
            'period',
            'notes',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        period_data = validated_data.pop('period')
        period, _ = LessonPeriod.objects.get_or_create(**period_data)
        validated_data['period'] = period
        return TimetableEntry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        period_data = validated_data.pop('period', None)
        if period_data:
            period, _ = LessonPeriod.objects.get_or_create(**period_data)
            instance.period = period
        return super().update(instance, validated_data)
