from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
     return 'user_{0}/{1}'.format(instance.user.id, filename)

class Image(models.Model):
	user = models.ForeignKey(User, default=3)
   	description = models.CharField(max_length=255, blank=True)
	image = models.ImageField(upload_to=user_directory_path)
	uploaded_at = models.DateTimeField(auto_now_add=True)