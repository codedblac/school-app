from rest_framework import serializers
from .models import Conversation, Message, ContactRestriction
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'


class ContactRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRestriction
        fields = '__all__'