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
  
  # for auditing
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super(ServerCategory, self).save(*args, **kwargs)

  def __str__(self):
    return self.name
  
  


class Server(models.Model):
  name = models.CharField(max_length=100)
  #delete server if owner deleted for now, look into ownership transferral later
  owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="server_owner")
  #leaving on delete to protect for now as we won't want to delete every server linked to the category
  category = models.ForeignKey(ServerCategory, on_delete=models.PROTECT, related_name="server_category")
  description = models.CharField(max_length=255, blank=True, null=True)
  members = models.ManyToManyField(Account)
  server_icon = CloudinaryField(
        'server icon',  
        folder='ServerIcons',  
        default='default_server_uxlg3a.jpg'
      )
  banner_image = CloudinaryField(
        'server banner',  
        folder='ServerIcons',  
        default='default_server_uxlg3a.jpg'
      )
  
      # for auditing
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"[{self.category}]: [{self.id}] - {self.name}"

class Channel(models.Model):
    # we want to get our choices for the chnnel
    text = 'text'
    voice = 'voice'

    CHANNEL_TYPE_CHOICES = [
        (text, 'Text'),
        (voice, 'Voice'),
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="channel_owner")
    type = models.CharField(
        max_length=5,
        choices=CHANNEL_TYPE_CHOICES,
        default=text,
    )

    # for now delete the channel if the server is deleted
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")
    # channel description, only applicable if channel is a text channel
    description = models.CharField(max_length=255, null=True, blank=True)
    # for auditing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
      # Null it out if it's a voice channel, as they don't have one
      if self.type == self.voice:
          self.description = None  
      self.name = self.name.lower()
      super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name