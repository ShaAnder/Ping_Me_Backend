from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ConversationModel, Messages

User = get_user_model()

class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        self.server_id = self.scope["url_route"]["kwargs"]["serverId"]
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]

        self.user = User.objects.get(id=1)  # Replace with self.scope["user"] when using real auth

        self.room_group_name = f"chat_s{self.server_id}_c{self.channel_id}"

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        message = content.get("message", "")

        conversation, _ = ConversationModel.objects.get_or_create(channel_id=self.channel_id)

        new_message = Messages.objects.create(
            conversation=conversation,
            sender=self.user,
            content=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": {
                    "id": new_message.id,
                    "sender": new_message.sender.username,
                    "content": new_message.content,
                    "timestamp": [
                        new_message.timestamp_create.isoformat(),
                        new_message.timestamp_update.isoformat()
                    ],
                }
            }
        )

    def chat_message(self, event):
        self.send_json({
            "message": event["message"]
        })

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        super().disconnect(close_code)
