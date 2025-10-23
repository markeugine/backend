from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from . import serializers
from . import models


class ManageDesignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Design objects.
    Only accessible to admin users.
    """
    queryset = models.Design.objects.all()
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def add_update(self, request, pk=None):
        """
        Custom endpoint for adding a progress update (with optional image + status).
        Example URL: /api/designs/<id>/add_update/
        """
        design = self.get_object()
        serializer = serializers.AddUpdateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(design, serializer.validated_data)
            return Response({"message": "Update added successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDesignsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Design.objects.filter(user=self.request.user)