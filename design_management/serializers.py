# from rest_framework import serializers
# from .models import Design
# from decimal import Decimal
# from appointment.serializers import AppointmentSerializer

# class DesignSerializer(serializers.ModelSerializer):
#     """Serializer for creating and updating Design instances."""
#     appointment = AppointmentSerializer()

#     class Meta:
#         model = Design
#         fields = '__all__'
#         read_only_fields = ['balance', 'updates', 'created_at', 'updated_at']


# class AddUpdateSerializer(serializers.Serializer):
#     """Serializer used when admin adds a progress update."""
#     message = serializers.CharField()
#     process_status = serializers.ChoiceField(choices=Design.PROCESS_STATUS_CHOICES, required=False)
#     payment_status = serializers.ChoiceField(choices=Design.PAYMENT_STATUS_CHOICES, required=False)
#     amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
#     image_file = serializers.ImageField(required=False)

#     def update(self, instance, validated_data):
#         instance.add_update(
#             message=validated_data.get('message'),
#             process_status=validated_data.get('process_status'),
#             payment_status=validated_data.get('payment_status'),
#             amount_paid=validated_data.get('amount_paid'),
#             image_file=validated_data.get('image_file')
#         )
#         return instance


from rest_framework import serializers
from .models import Design
from appointment.models import Appointment  # ✅ import this
from decimal import Decimal


class DesignSerializer(serializers.ModelSerializer):
    """Serializer for viewing and creating Design instances."""

    # ✅ Make user and appointment selectable (instead of nested)
    user = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Design._meta.get_field('user').remote_field.model.objects.all())
    appointment = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Appointment.objects.all())
    

    class Meta:
        model = Design
        fields = '__all__'
        read_only_fields = [
            'balance',
            'updates',
            'created_at',
            'updated_at',
        ]



class AddUpdateSerializer(serializers.Serializer):
    """Serializer for adding a design progress update."""
    message = serializers.CharField()
    process_status = serializers.ChoiceField(choices=Design.PROCESS_STATUS_CHOICES, required=False)
    payment_status = serializers.ChoiceField(choices=Design.PAYMENT_STATUS_CHOICES, required=False)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    image_file = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        """Call the model’s add_update() method to append a progress entry."""
        instance.add_update(
            message=validated_data.get('message'),
            process_status=validated_data.get('process_status'),
            payment_status=validated_data.get('payment_status'),
            amount_paid=validated_data.get('amount_paid'),
            image_file=validated_data.get('image_file')
        )
        return instance
