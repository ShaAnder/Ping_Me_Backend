from rest_framework import serializers

from .models import Messages


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    sender_avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = [
            "id",
            "sender_username",      # display name
            "sender_avatar_url",    # avatar url
            "content",
            "timestamp_created",
            "timestamp_updated",
        ]

    def get_sender_username(self, obj):
        # Get the Account model's username (display name)
        account = getattr(obj.sender, "account", None)
        if account and account.username:
            return account.username
        return obj.sender.username  # fallback to User.username

    def get_sender_avatar_url(self, obj):
        account = getattr(obj.sender, "account", None)
        if account and account.image:
            return account.image.url
        return None
