from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers, models


class ManageDesignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Design objects (Admin only).
    """
    queryset = models.Design.objects.all()
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'], url_path='add_update')
    def add_update(self, request, pk=None):
        """
        Add progress or payment updates to an existing Design instance.
        Example URL: /api/designs/<id>/add_update/
        """
        design = self.get_object()
        serializer = serializers.AddUpdateSerializer(data=request.data)

        if serializer.is_valid():
            updated_design = serializer.update(design, serializer.validated_data)
            return Response({
                "message": "Update added successfully.",
                "process_status": updated_design.process_status,
                "payment_status": updated_design.payment_status,
                "total_paid": str(updated_design.amount_paid),
                "balance": str(updated_design.balance),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDesignsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint for clients to view their own design records.
    """
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Design.objects.filter(user=self.request.user).order_by('-updated_at')
