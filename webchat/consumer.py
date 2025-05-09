from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        self.accept()
        # Manually add to group if not using the `groups` attribute:
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)

    def receive_json(self, content, **kwargs):
        # Expecting {"message": "hello"} from client
        message = content.get("message", "")
        # Broadcast to group with type 'chat.message'
        async_to_sync(self.channel_layer.group_send)(
            "chat",
            {
                "type": "chat.message",   # event type -> method chat_message
                "message": message,
            }
        )

    def chat_message(self, event):
        # Receives {'type': 'chat.message', 'message': ...}
        # Send JSON back to WebSocket
        self.send_json({"message": event["message"]})
