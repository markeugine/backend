from django.db import models
from django.conf import settings
from gallery.models import Attire

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
        ('denied', 'Denied'),
        ('cancelled', 'Cancelled'),
        ('archived', 'Archived'),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ('fitting', 'Fitting'),
        ('inquiry', 'Inquiry')
    ]

    attire_from_gallery = models.ForeignKey(
        Attire,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES,
        default='inquiry'
    )
    date = models.DateField() 
    time = models.CharField(max_length=255, null=True, blank=True)  
    image = models.ImageField(upload_to='appointment_images/', null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    not_come = models.BooleanField(default=False,null=True)
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


class FollowUpAppointment(models.Model):
    FOLLOW_UP_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('unsuccessful', 'Unsuccessful')
    ]
    CLIENT_RESPONSE_CHOICES = [
        ('none', 'None'),
        ('agreed', 'Agreed'),
        ('disagreed', 'Disagreed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follow_up',
        null=True, blank=True
    )
    admin_note = models.TextField(null=True, blank=True)
    for_fitting = models.BooleanField(default=False)
    date = models.DateField() 
    time = models.CharField()
    status = models.CharField(
        max_length=20,  
        choices=FOLLOW_UP_STATUS_CHOICES,
        default='pending'
    )
    project_id = models.CharField(blank=True, null=True)
    client_response = models.CharField(
        max_length=20,
        choices=CLIENT_RESPONSE_CHOICES,
        default='none'
    )
    client_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)