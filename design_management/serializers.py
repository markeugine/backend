from rest_framework import serializers
from .models import Design
from decimal import Decimal


class DesignSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Design instances."""
    class Meta:
        model = Design
        fields = '__all__'
        read_only_fields = ['balance', 'updates', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Automatically compute balance and payment status upon creation."""
        total_amount = Decimal(validated_data.get('total_amount', 0))
        amount_paid = Decimal(validated_data.get('amount_paid', 0))
        balance = total_amount - amount_paid

        if amount_paid <= 0:
            payment_status = 'no_payment'
        elif balance > 0:
            payment_status = 'partial_payment'
        elif balance == 0:
            payment_status = 'fully_paid'

        validated_data['balance'] = balance
        validated_data['payment_status'] = payment_status
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Prevent total_amount modification after creation."""
        validated_data.pop('total_amount', None)
        return super().update(instance, validated_data)


class AddUpdateSerializer(serializers.Serializer):
    """Serializer used when admin adds a progress update."""
    message = serializers.CharField()
    process_status = serializers.ChoiceField(choices=Design.PROCESS_STATUS_CHOICES, required=False)
    payment_status = serializers.ChoiceField(choices=Design.PAYMENT_STATUS_CHOICES, required=False)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    image_file = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        instance.add_update(
            message=validated_data.get('message'),
            process_status=validated_data.get('process_status'),
            payment_status=validated_data.get('payment_status'),
            amount_paid=validated_data.get('amount_paid'),
            image_file=validated_data.get('image_file')
        )
        return instance
