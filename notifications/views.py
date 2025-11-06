from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth import get_user_model


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Users see their own notifications; admins see all."""
        user = self.request.user
        return Notification.objects.filter(receiver=user)

    def perform_create(self, serializer):  
        """Used when creating notifications manually through the API."""
        if not serializer.validated_data.get("receiver"):
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
            serializer.save(receiver=admin_user)
        else:
            serializer.save()

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def mark_all_as_read(self, request):
        """Mark all notifications for current user as read."""
        Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all marked as read'}, status=status.HTTP_200_OK)
