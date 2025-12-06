from rest_framework import serializers
from . import models

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.

    Includes related user information (email, first name, last name, phone number)
    as read-only fields to display alongside the appointment details.

    The 'user' field is read-only and automatically set when creating appointments.
    """
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    phone_number = serializers.ReadOnlyField(source='user.phone_number')
    address = serializers.ReadOnlyField(source='user.address')
    facebook_link = serializers.ReadOnlyField(source='user.facebook_link')
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = models.Appointment
        fields = '__all__'
        read_only_fields = ['user']

    def get_image(self, obj):
        """Return full image URL (not just path)."""
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
    

class FollowUpAppointmentSerializer(serializers.ModelSerializer):
    """Basic serializer for FollowUpAppointment model."""
    
    class Meta:
        model = models.FollowUpAppointment
        fields = '__all__'
        read_only_fields = ['created_at']