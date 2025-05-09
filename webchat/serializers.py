from rest_framework import serializer
from .models import Messages

class MessageSerializer(serializer.ModelSerializer):
    sender = serializer.StringRelatedField()


    class Meta:
        model = Messages
        fields = ["id", "sender", "content", "timestamp_created", "timestamp_updated"]