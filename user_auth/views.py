from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from . import serializers
from .models import EmailOTP

# Retrieve the custom user model
User = get_user_model()


# NEW VIEWSET - Add this
class SendOTPViewSet(viewsets.ViewSet):
    """
    ViewSet to send OTP to user's email.
    Step 1 of registration process.
    """
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = serializers.SendOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate OTP
        otp_code = EmailOTP.generate_otp()
        
        # Save OTP to database
        EmailOTP.objects.create(email=email, otp_code=otp_code)
        
        # Send email with OTP
        try:
            subject = 'Your Verification Code'
            message = f'''
Hello,

Your verification code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Your App Team
            '''
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({
                'message': 'OTP sent successfully to your email',
                'email': email
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request):
        return Response({"detail": "Please POST email to send OTP."})


# NEW VIEWSET - Add this
class VerifyOTPViewSet(viewsets.ViewSet):
    """
    ViewSet to verify OTP code.
    Step 2 of registration process.
    """
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        try:
            # Get the latest OTP for this email
            otp = EmailOTP.objects.filter(
                email=email,
                otp_code=otp_code
            ).latest('created_at')
            
            # Check if OTP is valid
            if not otp.is_valid():
                return Response(
                    {'error': 'OTP has expired or already been used'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark OTP as verified
            otp.is_verified = True
            otp.save()
            
            return Response({
                'message': 'OTP verified successfully',
                'email': email,
                'verified': True
            }, status=status.HTTP_200_OK)
            
        except EmailOTP.DoesNotExist:
            return Response(
                {'error': 'Invalid OTP code'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def list(self, request):
        return Response({"detail": "Please POST email and OTP code to verify."})


class RegisterViewset(viewsets.ViewSet):
    """
    ViewSet for handling user registration.
    Step 3 - Final registration after OTP verification.
    Requires verified OTP before creating account.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def create(self, request):
        """
        Handles POST requests for registering a user.
        Validates OTP and saves the user data.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Save new user to the database
            user = serializer.save()
            
            # Generate auth token using knox
            _, token = AuthToken.objects.create(user)
            
            # Serialize user data for response
            user_data = serializers.UserInfoSerializer(user).data
            
            return Response({
                'message': 'Registration successful',
                'user': user_data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        
        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        return Response({"detail": "Please POST registration credentials here."})


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
    
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = serializers.UserInfoSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


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