from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import get_user_model, authenticate
from . import serializers

# Retrieve the custom user model
User = get_user_model()


class RegisterViewset(viewsets.ViewSet):
    """
    ViewSet for handling user registration.
    Allows any user to send a POST request to register a new account.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def create(self, request):
        """
        Handles POST requests for registering a user.
        Validates and saves the user data.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Save new user to the database
            serializer.save()
            return Response(serializer.data)
        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # To avoid the 405 - Method Not Allowed error.
    def list(self, request):
        return Response({"detail": "Please REGISTRATION credentials here."})


class LoginViewset(viewsets.ViewSet):
    """
    ViewSet for user login using email and password.
    Returns a token and user info upon successful authentication.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.LoginSerializer

    def create(self, request):
        """
        Handles POST requests for logging in a user.
        Validates credentials and returns a Knox token if successful.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate user using custom email-based backend
            user = authenticate(request, email=email, password=password)
            if user:
                # Generate auth token using knox
                _, token = AuthToken.objects.create(user)

                # Serialize user data for response
                user_data = serializers.UserInfoSerializer(user).data

                return Response(
                    {
                        'user': user_data,
                        'token': token,
                    }
                )
            else:
                # Return error if authentication fails
                return Response(
                    {"error": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # To avoid the 405 - Method Not Allowed error.
    def list(self, request):
        return Response({"detail": "Please POST your login credentials here."})


class AllUserViewSet(viewsets.ViewSet):
    """
    ViewSet to list all users in the system.
    Accessible only by admin users.
    """
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        """
        Handles GET requests to return a list of all users.
        """
        queryset = User.objects.all()
        # Serialize all users
        serializer = serializers.UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)


# ViewSet to return the authenticated user's profile info
class UserProfileViewSet(viewsets.ViewSet):
    """
    ViewSet to return the authenticated user's profile information.
    Accessible only by logged-in users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """
        Handles GET requests to retrieve the current user's profile data.
        """
        user = request.user
        # Serialize and return user's own info
        serializer = serializers.UserInfoSerializer(user)
        return Response(serializer.data)
