from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission:
    - Admins can do anything
    - Users can only access their own messages
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.sender == request.user or obj.receiver == request.user

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            # Admin sees all messages
            return Message.objects.all()
        # Regular user sees only their messages
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff:
            # Regular users can only send messages to admin
            admin_user = User.objects.filter(is_staff=True).first()
            serializer.save(sender=user, receiver=admin_user)
        else:
            # Admin can specify any receiver, ensure they exist
            receiver_id = self.request.data.get('receiver')
            if not receiver_id:
                raise serializer.ValidationError({"receiver": "This field is required."})
            receiver = User.objects.get(id=receiver_id)
            serializer.save(sender=user, receiver=receiver)

