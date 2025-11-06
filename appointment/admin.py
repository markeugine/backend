from django.contrib import admin
from . import models

# Appointment django's admin panel registration
admin.site.register(models.Appointment)
admin.site.register(models.FollowUpAppointment)
