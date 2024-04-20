from rest_framework import serializers
from .models import Staff, Attendance

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'department', 'email', 'adress', 'profile_image']

class AttendanceCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
