from django.contrib.auth import get_user_model
from django.db import models


class ConversationModel(models.Model):
    channel_id  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Messages(models.Model):
    conversation = models.ForeignKey(ConversationModel, on_delete=models.CASCADE, related_name="message")
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    content = models.TextField()
    timestamp_create = models.DateTimeField(auto_now_add=True)
    timestamp_update = models.DateTimeField(auto_now=True)