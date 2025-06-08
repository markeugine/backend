from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from . import serializers
from . import models


class SetUnavailabilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating, updating, or deleting unavailability records based on slot availability.
    If all slots are available (i.e., no unavailability), the record is deleted if it exists.
    """
    queryset = models.Unavailability.objects.all()
    serializer_class = serializers.SetUnavailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")

        if not date:
            return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if all slots are available (False = Available)
        all_available = not any([
            request.data.get("slot_one"),
            request.data.get("slot_two"),
            request.data.get("slot_three"),
            request.data.get("slot_four"),
            request.data.get("slot_five"),
        ])

        try:
            instance = models.Unavailability.objects.get(date=date)
            if all_available:
                instance.delete()
                return Response({"message": "Unavailability removed. All slots are available."}, status=status.HTTP_204_NO_CONTENT)
            else:
                # Update the record
                serializer = self.get_serializer(instance, data=request.data)
        except models.Unavailability.DoesNotExist:
            if all_available:
                return Response({"message": "No action taken. All slots are already available."}, status=status.HTTP_200_OK)
            else:
                # Create new record
                serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class DisplayUnavailabilityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for retrieving unavailability records.
    Supports optional filtering by date via query parameters.
    """
    queryset = models.Unavailability.objects.all()
    serializer_class = serializers.DisplayUnavailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        Retrieve a list of unavailability records.
        If 'date' query parameter is provided, filter the results by that date.

        Returns a JSON list of serialized unavailability objects.
        """
        date = request.query_params.get('date')
        queryset = self.get_queryset()

        if date:
            queryset = queryset.filter(date=date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
