from django.utils import timezone
from .models import Appointment

def archive_expired_appointments():
    today = timezone.now().date()

    # Find appointments in the past that are still pending
    expired = Appointment.objects.filter(
        appointment_status='pending',
        date__lt=today
    )

    count = expired.update(appointment_status='archived')
    print(f"✅ Archived {count} expired appointments")  