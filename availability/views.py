from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from . import serializers, models

class SetUnavailabilityViewSet(viewsets.ModelViewSet):
    queryset = models.Unavailability.objects.all()
    serializer_class = serializers.SetUnavailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def to_bool(self, value):
        if isinstance(value, bool):
            return value
        if value in ["true", "True", 1, "1"]:
            return True
        return False

    def slots_all_available(self, data):
        return not any([
            self.to_bool(data.get("slot_one")),
            self.to_bool(data.get("slot_two")),
            self.to_bool(data.get("slot_three")),
            self.to_bool(data.get("slot_four")),
            self.to_bool(data.get("slot_five")),
        ])

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")
        if not date:
            return Response({"error": "Date is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        all_available = self.slots_all_available(request.data)

        try:
            instance = models.Unavailability.objects.get(date=date)

            if all_available:
                instance.delete()
                return Response(
                    {"message": "Unavailability removed. All slots are available."},
                    status=status.HTTP_204_NO_CONTENT,
                )

            serializer = self.get_serializer(instance, data=request.data)

        except models.Unavailability.DoesNotExist:
            if all_available:
                return Response(
                    {"message": "No action taken. All slots are available."},
                    status=status.HTTP_200_OK
                )

            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if self.slots_all_available(serializer.validated_data):
            instance.delete()
            return Response(
                {"message": "Unavailability removed (all slots are available)."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)


class DisplayUnavailabilityViewSet(viewsets.ModelViewSet):
    queryset = models.Unavailability.objects.all()
    serializer_class = serializers.DisplayUnavailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        date = request.query_params.get("date")
        queryset = self.get_queryset()

        if date:
            queryset = queryset.filter(date=date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class Test(viewsets.ViewSet):
    pass 