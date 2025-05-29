from rest_framework import serializers
from .models import EventCategory, Event, EventAttendee

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description']

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    category = EventCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category', 'category_id', 'organizer', 'location',
            'start_datetime', 'end_datetime', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'organizer']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user
        return super().create(validated_data)

class EventAttendeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event = serializers.StringRelatedField(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source='event', write_only=True
    )

    class Meta:
        model = EventAttendee
        fields = ['id', 'event', 'event_id', 'user', 'rsvp_status', 'timestamp']
        read_only_fields = ['timestamp', 'user', 'event']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
