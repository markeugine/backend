from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from datetime import timedelta
import random


class CustomUserManager(BaseUserManager):
    """
    Custom manager for user model where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a required field!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that uses email instead of username for authentication.
    Includes additional fields like address, phone number, and social media links.
    """
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    first_name  = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_link = models.CharField(max_length=500, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# NEW MODEL - Add this to your existing models.py
class EmailOTP(models.Model):
    """
    Model to store OTP codes for email verification.
    OTPs expire after 10 minutes.
    """
    email = models.EmailField(max_length=250)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.otp_code}"
    
    def is_valid(self):
        """Check if OTP is still valid (not expired and not used)"""
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time and not self.is_verified
    
    @staticmethod
    def generate_otp():
        """Generate a random 6-digit OTP"""
        return str(random.randint(100000, 999999))