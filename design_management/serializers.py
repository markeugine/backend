from rest_framework import serializers
from .models import Design


class DesignSerializer(serializers.ModelSerializer):
    """
    Default serializer for Design model.
    """
    class Meta:
        model = Design
        fields = '__all__'


class AddUpdateSerializer(serializers.Serializer):
    """
    Serializer used when the admin adds a progress update to a Design.
    """
    message = serializers.CharField()
    process_status = serializers.ChoiceField(
        choices=Design.PROCESS_STATUS_CHOICES, 
        required=False
    )
    image_file = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        """
        Add a new update entry to the Design instance.
        """
        message = validated_data.get('message')
        process_status = validated_data.get('process_status', instance.process_status)
        image_file = validated_data.get('image_file')

        instance.add_update(message, process_status, image_file)
        return instance
