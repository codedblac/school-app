from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AIInteractionLog
from .serializers import AIInteractionLogSerializer

class AIInteractionLogViewSet(viewsets.ModelViewSet):
    queryset = AIInteractionLog.objects.all()
    serializer_class = AIInteractionLogSerializer

    @action(detail=False, methods=['post'])
    def query_ai(self, request):
        prompt = request.data.get('prompt')
        # Simulate AI response
        response = f"Simulated AI Response to: {prompt}"

        log = AIInteractionLog.objects.create(
            user=request.user,
            prompt=prompt,
            response=response
        )
        serializer = self.get_serializer(log)
        return Response(serializer.data)

