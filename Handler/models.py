from django.db import models


# Create your models here.
class QrCodeModel(models.Model):
    image = models.FileField(upload_to='qr_up_images/')
