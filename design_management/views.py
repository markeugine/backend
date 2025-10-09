from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
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


class UserDesignsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.DesignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Design.objects.filter(user=self.request.user)