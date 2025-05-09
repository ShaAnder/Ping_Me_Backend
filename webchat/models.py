from django.contrib.auth import get_user_model
from django.db import models


class ConversationModel(models.Model):
    channel_id  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Messages(models.Model):
    conversation = models.ForeignKey(ConversationModel, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    content = models.TextField()
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)