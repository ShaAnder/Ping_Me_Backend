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
        # pull both IDs out of the URL
        self.server_id  = self.scope["url_route"]["kwargs"]["serverId"]
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]

        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return


        # build one unique room name, to prevent same id diff server
        self.room_group_name = f"chat_s{self.server_id}_c{self.channel_id}"
        
        # accept the WS, then join the correctly‑named group
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        channel_id = self.channel_id
        sender = self.user
        message = content["message"]

        conversation, created = ConversationModel.objects.get_or_create(channel_id=channel_id)

        new_message = Messages.objects.create(conversation=conversation, sender=sender, content=message)

        # only broadcast to the exact room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "new_message": {
                    "id": new_message.id,
                    "sender": new_message.sender.username,
                    "content": new_message.content,
                    "timestamp": [new_message.timestamp_created.isoformat(), new_message.timestamp_updated.isoformat()],
                }
                
            }
        )

    def chat_message(self, event):
        # send only to sockets in this same room_group_name
        self.send_json({
            "message": event["new_message"]
        })

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.channel_id, self.channel_name)
        super().disconnect(close_code)