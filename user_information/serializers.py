# serializers.py
from rest_framework import serializers
from .models import UserInformation
from django.contrib.auth import get_user_model

User = get_user_model()

class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = [
            'id',
            'user',
            'height',
            'weight',
            'chest',
            'waist',
            'hips',
            'shoulder_width',
            'arm_length',
            'leg_length',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create measurement and set has_messurements to True for the user"""
        user_information = UserInformation.objects.create(**validated_data)
        
        # Update user's has_messurements to True
        user = validated_data.get('user')
        if user:
            user.has_messurements = True
            user.save()
        
        return user_information

    def update(self, instance, validated_data):
        """Update measurement and ensure has_messurements is True"""
        user_information = super().update(instance, validated_data)
        
        # Ensure user's has_messurements is set to True
        user = user_information.user
        if user and not user.has_messurements:
            user.has_messurements = True
            user.save()
        
        return user_information