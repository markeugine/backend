from rest_framework import serializers
from . import models

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.

    Includes related user information (email, first name, last name, phone number)
    as read-only fields to display alongside the appointment details.

    The 'user' field is read-only and automatically set when creating appointments.
    """
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = models.Appointment
        fields = '__all__'
        read_only_fields = ['user']


class DesignSerializer(serializers.ModelSerializer):
    """
    Serializer for Design model.
    """
    class Meta:
        model = models.Design
        fields = '__all__'