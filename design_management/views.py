


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers, models


class ManageDesignViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing all Design records.
    Admin can view, create, edit, delete, and add progress updates.
    """
    queryset = models.Design.objects.all().select_related('user', 'appointment')
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        """Admin can create a new design instance."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        design = serializer.save()
        return Response({
            "message": "Design created successfully.",
            "data": self.get_serializer(design).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='add_update')
    def add_update(self, request, pk=None):
        """
        POST /designs/{id}/add_update/
        Add a progress update to a specific design.
        """
        design = self.get_object()
        serializer = serializers.AddUpdateSerializer(data=request.data)

        if serializer.is_valid():
            updated_design = serializer.update(design, serializer.validated_data)
            return Response({
                "message": "Update added successfully.",
                "data": self.get_serializer(updated_design).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDesignsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Client ViewSet for viewing their own design progress and details.
    Accessible only by authenticated users.
    """
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Design.objects.filter(user=self.request.user).select_related('appointment').order_by('-updated_at')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse
import csv
from .models import Design

class ExportDesignsCSV(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="designs.csv"'

        writer = csv.writer(response)
        # CSV header
        writer.writerow([
            "ID", "User Email", "First Name", "Last Name", "Phone Number",
            "Appointment Date", "Attire Type", "Targeted Date", "Fitting Date", "Fitting Time",
            "Fitting Successful", "Process Status", "Payment Status",
            "Total Amount", "Amount Paid", "Balance", "Description",
            "Created At", "Updated At", "Reference Image", "Updates JSON"
        ])

        for d in Design.objects.all():
            writer.writerow([
                d.id,
                d.email,
                d.first_name,
                d.last_name,
                d.phone_number,
                d.appointment_date,
                d.attire_type,
                d.targeted_date,
                d.fitting_date or "",
                d.fitting_time or "",
                d.fitting_successful,
                d.process_status,
                d.payment_status,
                d.total_amount,
                d.amount_paid,
                d.balance,
                d.description or "",
                d.created_at,
                d.updated_at,
                d.reference_image or "",
                d.updates,
            ])

        return response