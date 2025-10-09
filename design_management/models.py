from django.db import models
from django.conf import settings


# Create your models here.
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
        'appointment.Appointment',
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
    description = models.TextField(
        blank=True, 
        null=True
    )
    reference_image = models.ImageField(
        upload_to="design_references/", 
        blank=True, 
        null=True
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



