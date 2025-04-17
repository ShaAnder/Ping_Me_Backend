from cloudinary.models import CloudinaryField
from django.db import models

from account.models import Account


class ServerCategory(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  category_image = CloudinaryField(
        'image',  
        folder='ServerCategories',  
        default='default_server_uxlg3a.jpg'
      )
  
  def __str__(self):
    return self.name


class Server(models.Model):
  name = models.CharField(max_length=100)
  #delete server if owner deleted for now, look into ownership transferral later
  owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="server_owner")
  #leaving on delete to protect for now as we won't want to delete every server linked to the category
  category = models.ForeignKey(ServerCategory, on_delete=models.PROTECT, related_name="server_category")
  description = models.CharField(max_length=255, null=True)
  members = models.ManyToManyField(Account)
  server_image = CloudinaryField(
        'image',  
        folder='ServerIcons',  
        default='default_server_uxlg3a.jpg'
      )

