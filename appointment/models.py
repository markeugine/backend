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
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    date = models.DateField()  # Date of the appointment (e.g., 2025-05-14)
    time = models.CharField(max_length=255, null=True, blank=True)  # Optional time or slot description

    image = models.ImageField(upload_to='appointment_images/', null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
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
    
    def __str__(self):
        """Return a human-readable string representation of the appointment."""
        return f"{self.first_name} {self.last_name} - {self.date}"

    class Meta:
        ordering = ['-updated_at']


class Design(models.Model):
    """
    Model representing a design project for an approved appointment.

    Fields:
        - user: ForeignKey linking to the user who owns the design
        - appointment: ForeignKey linking to the related appointment
        - attire_type: Type of attire being designed
        - targeted_date: Expected completion date
        - process_status: Current status of the design process
        - payment_status: Current payment status
        - amount_paid: Amount paid so far
    """

    PROCESS_STATUS_CHOICES = [
        ('designing', 'Designing'),
        ('materializing', 'Materializing'),
        ('ready', 'Ready'),
        ('done', 'Done'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('no_payment', 'No Payment'),
        ('partial_payment', 'Partial Payment'),
        ('fully_paid', 'Fully Paid'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='designs'
    )
    
    appointment = models.OneToOneField(
        'Appointment',
        on_delete=models.CASCADE,
        related_name='design'
    )

    attire_type = models.CharField(max_length=100)
    targeted_date = models.DateField()
    process_status = models.CharField(
        max_length=20,
        choices=PROCESS_STATUS_CHOICES,
        default='designing'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='no_payment'
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def email(self):
        """Return the email address of the user who owns the design."""
        return self.user.email
    
    @property
    def first_name(self):
        """Return the first name of the user who owns the design."""
        return self.user.first_name

    @property
    def last_name(self):
        """Return the last name of the user who owns the design."""
        return self.user.last_name

    @property
    def phone_number(self):
        """Return the phone number of the user who owns the design."""
        return self.user.phone_number

    @property
    def appointment_date(self):
        """Return the date of the associated appointment."""
        return self.appointment.date

    def __str__(self):
        """Return a human-readable string representation of the design."""
        return f"Design for {self.first_name} {self.last_name} - {self.attire_type}"

    class Meta:
        ordering = ['-updated_at']



