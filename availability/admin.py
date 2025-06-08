from django.contrib import admin
from . import models

# Unavailability django's admin panel registration
admin.site.register(models.Unavailability)
