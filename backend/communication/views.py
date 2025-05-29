from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Conversation, Message, ContactRestriction
from .serializers import ConversationSerializer, MessageSerializer, ContactRestrictionSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save(created_by=self.request.user)
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ContactRestrictionViewSet(viewsets.ModelViewSet):
    queryset = ContactRestriction.objects.all()
    serializer_class = ContactRestrictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)