from django.contrib import admin
from . import models 

# Custom user django's admin panel registration
admin.site.register(models.CustomUser)
