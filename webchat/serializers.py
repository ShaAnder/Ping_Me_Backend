from rest_framework import serializers

from .models import Messages


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()


    class Meta:
        model = Messages
        fields = ["id", "sender", "content", "timestamp_created", "timestamp_updated"]