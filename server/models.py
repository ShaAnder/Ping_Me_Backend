from django.db import models
from cloudinary.models import CloudinaryField


class ServerCategory(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  server_image = CloudinaryField(
        'image',  
        folder='ServerIcons',  
        default='default_server_uxlg3a.jpg'
      )


class Server(models.Model):
  pass
