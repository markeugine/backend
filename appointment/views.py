from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from . import serializers, models


def auto_archive_expired():
    today = timezone.now().date()
    models.Appointment.objects.filter(
        appointment_status='pending',
        date__lt=today
    ).update(appointment_status='archived')


class SetAppointmentViewSet(viewsets.ViewSet):
    serializer_class = serializers.AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Appointment created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentsListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        # ✅ Auto archive before sending data
        auto_archive_expired()

        appointments = models.Appointment.objects.all()
        serializer = serializers.AppointmentSerializer(
            appointments, many=True, context={'request': request}
        )
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

    def retrieve(self, request, pk=None):
        try:
            appointment = models.Appointment.objects.get(pk=pk)
        except models.Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.AppointmentSerializer(
            appointment, context={'request': request}
        )
        return Response(serializer.data)


class UserAppointmentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def list(self, request):
        # ✅ Auto archive before fetching user's data
        auto_archive_expired()

        user = request.user
        appointments = models.Appointment.objects.filter(user=user)
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        except models.Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        # 🔥 CAPTURE OLD STATUS BEFORE UPDATE
        old_status = appointment.appointment_status
        new_status = request.data.get('appointment_status')

        # Update the appointment
        serializer = serializers.AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            # 🔥 INCREMENT CANCEL COUNTER IF APPROVED APPOINTMENT IS CANCELLED
            user_cancels = None
            if new_status == 'cancelled' and old_status == 'approved':
                user = request.user
                user.cancels += 1
                user.save(update_fields=['cancels'])
                user_cancels = user.cancels
            
            # Prepare response
            response_data = serializer.data
            
            # Add cancel count to response if it was incremented
            if user_cancels is not None:
                response_data['user_cancels'] = user_cancels
            
            return Response(response_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowUpAppointmentViewSet(viewsets.ModelViewSet):
    queryset = models.FollowUpAppointment.objects.all()
    serializer_class = serializers.FollowUpAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(user=self.request.user)
        else:
            serializer.save()



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import csv
from django.http import HttpResponse
from .models import Appointment


class ExportAppointmentsCSV(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="appointments.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "ID", "Email", "First Name", "Last Name", "Phone Number",
            "Address", "Facebook Link", "Appointment Type", "Date", "Time",
            "Description", "Not Come", "Attire From Gallery", "Status",
            "Created At", "Updated At", "Image URL"
        ])

        for a in Appointment.objects.all():
            writer.writerow([
                a.id,
                a.email,
                a.first_name,
                a.last_name,
                a.phone_number,
                a.address,
                a.facebook_link,
                a.appointment_type,
                a.date,
                a.time,
                a.description,
                a.not_come,
                a.attire_from_gallery.id if a.attire_from_gallery else "",
                a.appointment_status,
                a.created_at,
                a.updated_at,
                a.image.url if a.image else ""
            ])

        return response
