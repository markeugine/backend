from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'receiver',
            'header',
            'message',
            'link',
            'is_read',
            'is_system',
            'created_at',
            'is_archived'
        ]
        read_only_fields = ['id', 'created_at']