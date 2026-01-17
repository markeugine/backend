from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action
from .models import Attire
from .serializers import AttireSerializer


class AttireAdminViewSet(viewsets.ModelViewSet):
    queryset = Attire.objects.all().order_by('-created_at')
    serializer_class = AttireSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Attire.objects.all().order_by('-created_at')
        show_archived = self.request.query_params.get('show_archived')
        if show_archived == "true":
            return queryset
        return queryset.filter(is_archived=False)

    def update(self, request, *args, **kwargs):
        """
        Handle full or partial updates for any field of the Attire model.
        """
        partial = kwargs.pop('partial', False)  # False for PUT, True for PATCH
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class AttireUserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User can only view NON-ARCHIVED attires where `to_show` is true.
    """

    serializer_class = AttireSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Attire.objects.filter(
            is_archived=False
        ).order_by('-created_at')
