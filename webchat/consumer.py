import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = "testserver"

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.server_id,
            self.channel_name,
        )

    def receive(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.server_id, 
            {
                "type": "chat.message", 
                "new_message": content["message"]
            },
        )

    def chat_message(self, event):
        self.send_json(event)

    def disconnect(self, close_code):
        pass