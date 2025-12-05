from rest_framework import serializers
from . import models

class SetUnavailabilitySerializer(serializers.ModelSerializer):
    DEFAULT_REASON = "Designer not available"
    AVAILABLE_REASON = "Available"

    class Meta:
        model = models.Unavailability
        fields = '__all__'

    def validate(self, data):
        slot_reason_pairs = [
            ("slot_one", "reason_one"),
            ("slot_two", "reason_two"),
            ("slot_three", "reason_three"),
            ("slot_four", "reason_four"),
            ("slot_five", "reason_five"),
        ]

        for slot, reason in slot_reason_pairs:
            slot_value = data.get(slot)
            reason_value = data.get(reason)

            # Slot unavailable → must have a valid reason
            if slot_value:
                if not reason_value or reason_value == "" or reason_value == self.AVAILABLE_REASON:
                    data[reason] = self.DEFAULT_REASON
            else:
                data[reason] = self.AVAILABLE_REASON

        return data


class DisplayUnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unavailability
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]
