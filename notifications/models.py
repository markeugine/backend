from django.db import models
from django.conf import settings


class Notification(models.Model):
    # Who will receive the notification
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications',
        null=True,
        blank=True
    )
    
    header = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    # For system or auto-generated notifications
    is_system = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.header} → {self.receiver.email}"
