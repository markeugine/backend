from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework.parsers import MultiPartParser, FormParser



class SetAppointmentViewSet(viewsets.ViewSet):
    """
    ViewSet to allow authenticated users to create new appointments.
    """
    serializer_class = serializers.AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    def create(self, request, *args, **kwargs):
        """
        Create a new appointment for the authenticated user.
        
        Expects appointment data in request.data.
        Returns success message or validation errors.
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            # Save the appointment linked to the current user
            serializer.save(user=request.user)

            return Response(
                {"message": "Appointment created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from . import models, serializers


class AppointmentsListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        appointments = models.Appointment.objects.all()
        serializer = serializers.AppointmentSerializer(appointments, many=True, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            appointment = models.Appointment.objects.get(pk=pk)
        except models.Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.AppointmentSerializer(
            appointment, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserAppointmentsViewSet(viewsets.ViewSet):
    """
    ViewSet for authenticated users to manage their own appointments.
    Supports listing, partial updating, and deleting.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        List all appointments belonging to the authenticated user.
        """
        user = request.user
        appointments = models.Appointment.objects.filter(user=user)
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
        
    def partial_update(self, request, pk=None):
        """
        Partially update an appointment owned by the authenticated user.
        Prevents updating the 'appointment_status' field.
        """
        appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        
        # Make a mutable copy of request data and remove 'appointment_status'
        data = request.data.copy()

        serializer = serializers.AppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an appointment owned by the authenticated user.
        """
        appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


