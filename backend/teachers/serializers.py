from rest_framework import serializers
from .models import Teacher
from accounts.serializers import UserSerializer

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'