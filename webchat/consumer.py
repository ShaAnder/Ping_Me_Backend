from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = "testserver"

    def connect(self):
        print("WebSocket connected:", self.channel_name)
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.server_id,
            self.channel_name,
        )

    def receive_json(self, content):
        print("Received message from client:", content)
        async_to_sync(self.channel_layer.group_send)(
            self.server_id,
            {
                "type": "chat.message",
                "new_message": content["message"],
            },
        )

    def chat_message(self, event):
        print("Broadcasting message to client:", event)
        self.send_json(event)

    def disconnect(self, close_code):
        print("WebSocket disconnected:", self.channel_name)
