# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserInformation
from .serializers import UserInformationSerializer

class IsAdminOrReadOnlySelf(permissions.BasePermission):
    """
    Custom permission:
    - Admins can view, create, edit all measurements
    - Users can only view their own measurements (read-only)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.is_staff:
            return True
        # Users can only view their own measurements
        return obj.user == request.user and request.method in permissions.SAFE_METHODS


class UserInformationViewSet(viewsets.ModelViewSet):
    """
    - Admins: View, create, edit, delete all user measurements
    - Users: View only their own measurements (read-only)
    """
    serializer_class = UserInformationSerializer
    permission_classes = [IsAdminOrReadOnlySelf]

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        if user_id:
            return UserInformation.objects.filter(user_id=user_id)
        return UserInformation.objects.all()

    def perform_create(self, serializer):
        """
        Admins can create measurements for any user.
        Users cannot create (no permission).
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            return Response(
                {'detail': 'You do not have permission to create measurements.'},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        """
        Admins can update measurements for any user.
        Users cannot update (no permission).
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            return Response(
                {'detail': 'You do not have permission to edit measurements.'},
                status=status.HTTP_403_FORBIDDEN
            )

    def perform_destroy(self, instance):
        """
        Only admins can delete measurements.
        """
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to delete measurements.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrReadOnlySelf])
    def my_measurements(self, request):
        """
        Get current user's own measurements.
        Users: GET /user_info/user-information/my_measurements/
        """
        user_info = UserInformation.objects.filter(user=request.user).first()
        if user_info:
            serializer = self.get_serializer(user_info)
            return Response(serializer.data)
        return Response({'detail': 'No measurements found.'}, status=status.HTTP_404_NOT_FOUND)