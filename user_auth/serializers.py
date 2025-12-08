from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmailOTP
from django.utils import timezone

# Get the custom user model
User = get_user_model()


# NEW SERIALIZERS - Add these
class SendOTPSerializer(serializers.Serializer):
    """Serializer for sending OTP to email"""
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying OTP"""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=6)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. Handles validation and user creation.
    """
    otp_code = serializers.CharField(max_length=6, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'otp_code',
            'username',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'facebook_link',
            'has_messurements',
            'cancels'  # Added
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'cancels': {'read_only': True}  # Should not be set during registration
        }

    def validate(self, data):
        """Verify OTP before allowing registration"""
        email = data['email']
        otp_code = data['otp_code']
        
        try:
            otp = EmailOTP.objects.filter(
                email=email,
                otp_code=otp_code,
                is_verified=True
            ).latest('created_at')
            
            # Check if OTP was verified recently (within 30 minutes)
            if (timezone.now() - otp.created_at).seconds > 1800:
                raise serializers.ValidationError({
                    "otp_code": "OTP has expired. Please request a new one."
                })
                
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({
                "otp_code": "Invalid or unverified OTP. Please verify your email first."
            })
        
        return data

    def create(self, validated_data):
        # Remove OTP code before creating user
        validated_data.pop('otp_code')
        
        # Use the custom user manager's create_user method
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Accepts email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        # Exclude the password field from the output
        to_return = super().to_representation(instance)
        to_return.pop('password', None)
        return to_return


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user information. All fields are read-only.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'address',
            'facebook_link',
            'phone_number',
            'is_staff',
            'is_superuser',
            'has_messurements',
            'cancels'  # Added
        ]
        read_only_fields = fields


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    Allows users to update their profile details.
    """
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'facebook_link',
        ]
        
    def update(self, instance, validated_data):
        """Update and return the user instance"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance