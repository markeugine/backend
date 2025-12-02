from django.db import models

class Unavailability(models.Model):
    # ✅ Predefined reasons
    REASONS = [
        ('Designer not available', 'Designer not available'),
        ('Scheduled Appointment', 'Scheduled Appointment'),
        ('Scheduled Fitting', 'Scheduled Fitting'),
        ('Available', 'Available'),  # ← add this
    ]

    DEFAULT_REASON = 'Designer not available'

    date = models.DateField(unique=True)

    slot_one = models.BooleanField(default=False)
    reason_one = models.CharField(
        max_length=255,
        choices=REASONS,
        default=DEFAULT_REASON,
        blank=True,
        null=True
    )

    slot_two = models.BooleanField(default=False)
    reason_two = models.CharField(
        max_length=255,
        choices=REASONS,
        default=DEFAULT_REASON,
        blank=True,
        null=True
    )

    slot_three = models.BooleanField(default=False)
    reason_three = models.CharField(
        max_length=255,
        choices=REASONS,
        default=DEFAULT_REASON,
        blank=True,
        null=True
    )

    slot_four = models.BooleanField(default=False)
    reason_four = models.CharField(
        max_length=255,
        choices=REASONS,
        default=DEFAULT_REASON,
        blank=True,
        null=True
    )

    slot_five = models.BooleanField(default=False)
    reason_five = models.CharField(
        max_length=255,
        choices=REASONS,
        default=DEFAULT_REASON,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Unavailable on {self.date}"
