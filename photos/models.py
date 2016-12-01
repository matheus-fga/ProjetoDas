from django.db import models

class Image(models.Model):
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
