# from rest_framework import permissions, viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from . import serializers, models


# class ManageDesignViewSet(viewsets.ModelViewSet):
#     queryset = models.Design.objects.all()
#     serializer_class = serializers.DesignSerializer
#     permission_classes = [permissions.IsAdminUser]


#     @action(detail=True, methods=['post'], url_path='add_update')
#     def add_update(self, request, pk=None):
#         design = self.get_object()
#         serializer = serializers.AddUpdateSerializer(data=request.data)

#         if serializer.is_valid():
#             updated_design = serializer.update(design, serializer.validated_data)
#             return Response({
#                 "message": "Update added successfully.",
#                 "process_status": updated_design.process_status,
#                 "payment_status": updated_design.payment_status,
#                 "total_paid": str(updated_design.amount_paid),
#                 "balance": str(updated_design.balance),
#             }, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UserDesignsViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Endpoint for clients to view their own design records.
#     """
#     serializer_class = serializers.DesignSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return models.Design.objects.filter(user=self.request.user).order_by('-updated_at')




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
