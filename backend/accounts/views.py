from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()  # Correct way to reference the custom user model

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
