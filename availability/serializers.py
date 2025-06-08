from rest_framework import serializers
from . import models


class SetUnavailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating unavailability entries.
    Includes specific fields relevant for setting unavailability slots.
    """
    class Meta:
        model = models.Unavailability
        fields = [
            'id',
            'date',
            'slot_one',
            'slot_two',
            'slot_three',
            'slot_four',
            'slot_five',
        ]


class DisplayUnavailabilitySerializer(serializers.ModelSerializer):
    """
    Serializer for displaying unavailability records.
    All fields from the model are included and set as read-only.
    """
    class Meta:
        model = models.Unavailability
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]
