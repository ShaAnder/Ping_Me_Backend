from rest_framework import serializers

from account.serializers import AccountSerializer

from .models import Messages


class MessageSerializer(serializers.ModelSerializer):
    user = AccountSerializer(source='sender.account', read_only=True)

    class Meta:
        model = Messages
        fields = [
            "id",
            "user",
            "content",
            "timestamp_created",
            "timestamp_updated",
        ]