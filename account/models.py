# using abstract user as a starting point
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Account(models.Model):
    """User model for accounts

    Args:
        User (model_baseclass): default django user model
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True)
    image = CloudinaryField(
        "image", folder="Avatars", default="default_profile_uxlg3a.jpg", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}"


def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(owner=instance, username=instance.username)
        


post_save.connect(create_account, sender=User)
