from django.db import models
from django.conf import settings


class Appointment(models.Model):
    """
    Model representing an appointment made by a user.

    Fields:
        - user: ForeignKey linking to the user who made the appointment.
        - date: The date for the appointment.
        - time: Optional time description or slot for the appointment.
        - image: Optional image related to the appointment (e.g., reference photo).
        - address: Optional address where the appointment will take place.
        - facebook_link: Optional Facebook profile or event link related to the appointment.
        - description: Optional detailed description or notes for the appointment.
        - appointment_status: Status of the appointment (default 'pending').
        - created_at: Timestamp when the appointment was created.
        - updated_at: Timestamp when the appointment was last updated.
    """

    APPOINTMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    date = models.DateField() 
    time = models.CharField(max_length=255, null=True, blank=True)  
    image = models.ImageField(upload_to='appointment_images/', null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    appointment_status = models.CharField(
        max_length=20,
        choices=APPOINTMENT_STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def email(self):
        """Return the email address of the user who created the appointment."""
        return self.user.email
    
    @property
    def first_name(self):
        """Return the first name of the user who created the appointment."""
        return self.user.first_name

    @property
    def last_name(self):
        """Return the last name of the user who created the appointment."""
        return self.user.last_name

    @property
    def phone_number(self):
        """Return the phone number of the user who created the appointment."""
        return self.user.phone_number  
    
    @property
    def address(self):
        return self.user.address

    @property
    def facebook_link(self):
        return self.user.facebook_link
    
    def __str__(self):
        """Return a human-readable string representation of the appointment."""
        return f"{self.first_name} {self.last_name} - {self.date}"

    class Meta:
        ordering = ['-updated_at']