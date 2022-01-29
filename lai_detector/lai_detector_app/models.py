from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    path = models.CharField("path", max_length=255, null=True)
    detected_path = models.CharField("detected_path", max_length=255, null=True)
    output_path = models.CharField("output_path", max_length=255, null=True)

    image_file = models.ImageField(upload_to='images/%d_%m_%Y_%H_%M_%S/', blank=True, null=True)
    detected_image_file = models.ImageField(upload_to='images/%d_%m_%Y_%H_%M_%S/detected/', blank=True, null=True)
    detected_output_image_file = models.ImageField(upload_to='images/%d_%m_%Y_%H_%M_%S/detected_output/', blank=True, null=True)
