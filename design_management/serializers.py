from rest_framework import serializers
from . import models

class DesignSerializer(serializers.ModelSerializer):
    """
    Serializer for Design model.
    """
    class Meta:
        model = models.Design
        fields = '__all__'