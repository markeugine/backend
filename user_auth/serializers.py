from rest_framework import serializers
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. Handles validation and user creation.
    """
    class Meta:
        model = User  # Use the custom user model
        fields = [
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
            'address',
            'phone_number',
            'facebook_link',
        ]
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        # Use the custom user manager's create_user method
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Accepts email and password.
    """
    email = serializers.EmailField()  # Email field for login
    password = serializers.CharField()  # Password field for login

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
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = fields  # Make all fields read-only
