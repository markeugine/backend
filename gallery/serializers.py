from rest_framework import serializers
from .models import Attire

class AttireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attire
        fields = '__all__'  # includes all fields
        read_only_fields = ['id', 'created_at', 'updated_at']  # optional
