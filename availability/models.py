from django.db import models

class Unavailability(models.Model):
    """
    Model to represent unavailability for specific dates and time slots.
    Each date can have multiple time slots marked as unavailable.
    
    Fields:
        - date: Unique date for the unavailability record.
        - slot_one to slot_five: Boolean flags indicating unavailability during specific time slots.
    """
    date = models.DateField(unique=True)

    # Morning and afternoon time slots with their respective time ranges
    slot_one = models.BooleanField(default=False)   # 7:00 - 8:30 AM
    slot_two = models.BooleanField(default=False)   # 8:30 - 10:00 AM
    slot_three = models.BooleanField(default=False) # 10:00 - 11:30 AM
    slot_four = models.BooleanField(default=False)  # 1:00 - 2:30 PM
    slot_five = models.BooleanField(default=False)  # 2:30 - 4:00 PM

    def __str__(self):
        """
        Return a human-readable string representation of the object,
        indicating the date of unavailability.
        """
        return f"Unavailable on {self.date}"
