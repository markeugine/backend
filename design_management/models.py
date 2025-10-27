from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import default_storage

class Design(models.Model):
    """
    Model representing a design project for an approved appointment.
    Automatically calculates balance and payment status when created
    or when payments are added.
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

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total price of the gown or design project."
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total amount paid by the client so far."
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Remaining balance = total_amount - amount_paid."
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    updates = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "List of updates or progress logs related to this design. "
            "Each entry includes: message, process_status, payment_status, "
            "amount_paid, added_payment, balance, image, and timestamp."
        )
    )

    def save(self, *args, **kwargs):
        """Automatically update balance and payment status when saving."""
        self.balance = self.total_amount - self.amount_paid

        # ✅ Ensure full payment when balance == 0
        if self.amount_paid <= 0:
            self.payment_status = 'no_payment'
        elif self.balance == 0:
            self.payment_status = 'fully_paid'
        else:
            self.payment_status = 'partial_payment'

        super().save(*args, **kwargs)

    def add_update(self, message, process_status=None, payment_status=None, amount_paid=None, image_file=None):
        """Add a progress update with optional payment and image."""
        image_url = None

        if image_file:
            image_path = default_storage.save(f"design_updates/{image_file.name}", image_file)
            image_url = default_storage.url(image_path)

        if process_status is None:
            process_status = self.process_status
        if payment_status is None:
            payment_status = self.payment_status

        # ✅ Add payment cumulatively
        if amount_paid is not None:
            new_total_paid = self.amount_paid + amount_paid
        else:
            new_total_paid = self.amount_paid

        # ✅ Compute new balance
        new_balance = self.total_amount - new_total_paid

        # ✅ Fix: handle full payment when balance == 0
        if new_total_paid <= 0:
            payment_status = 'no_payment'
        elif new_balance == 0:
            payment_status = 'fully_paid'
        else:
            payment_status = 'partial_payment'

        # Create update log entry
        update_entry = {
            "message": message,
            "process_status": process_status,
            "payment_status": payment_status,
            "amount_paid_total": str(new_total_paid),
            "added_payment": str(amount_paid or 0.00),
            "balance": str(new_balance),
            "image": image_url,
            "timestamp": timezone.now().isoformat(),
        }

        self.updates.append(update_entry)

        # Update instance
        self.process_status = process_status
        self.payment_status = payment_status
        self.amount_paid = new_total_paid
        self.balance = new_balance
        self.save()

    @property
    def email(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def phone_number(self):
        return self.user.phone_number

    @property
    def appointment_date(self):
        return self.appointment.date

    @property
    def reference_image(self):
        """Fetch the reference image from the related appointment, if it exists."""
        if hasattr(self.appointment, 'reference_image') and self.appointment.reference_image:
            return self.appointment.reference_image.url
        return None

    def __str__(self):
        return f"Design for {self.first_name} {self.last_name} - {self.attire_type}"

    class Meta:
        ordering = ['-updated_at']
