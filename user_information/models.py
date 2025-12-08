from django.db import models
from django.conf import settings

class UserInformation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_information'
    )

    height = models.CharField(max_length=50, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    chest = models.CharField(max_length=50, null=True, blank=True)
    waist = models.CharField(max_length=50, null=True, blank=True)
    hips = models.CharField(max_length=50, null=True, blank=True)
    shoulder_width = models.CharField(max_length=50, null=True, blank=True)
    arm_length = models.CharField(max_length=50, null=True, blank=True)
    leg_length = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Measurements"