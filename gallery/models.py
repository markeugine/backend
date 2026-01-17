from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os

def attire_image_upload_path(instance, filename):
    attire_folder = slugify(instance.attire_name)
    return os.path.join("gallery_images", attire_folder, filename)

class Attire(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attires',
        blank=True,
        null=True
    )
    
    attire_name = models.CharField(max_length=255)
    attire_type = models.CharField(max_length=255)
    attire_description = models.TextField()
    to_show = models.BooleanField(default=True)
    landing_page = models.BooleanField(default=False)
    total_price = models.CharField(
        max_length=255,
        default=None,
        blank=True
    )

    # Store images inside a folder named after the attire
    image1 = models.ImageField(upload_to=attire_image_upload_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=attire_image_upload_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=attire_image_upload_path, blank=True, null=True)
    image4 = models.ImageField(upload_to=attire_image_upload_path, blank=True, null=True)
    image5 = models.ImageField(upload_to=attire_image_upload_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.attire_name
