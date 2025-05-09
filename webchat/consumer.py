from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        # pull both IDs out of the URL
        self.server_id  = self.scope["url_route"]["kwargs"]["serverId"]
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]

        # build one unique room name
        self.room_group_name = f"chat_s{self.server_id}_c{self.channel_id}"
        
        # accept the WS, then join the correctly‑named group
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.channel_id, self.channel_name)

    def receive_json(self, content, **kwargs):
        message = content.get("message", "").strip()
        # early return guard
        if not message:
            return
        
        # only broadcast to the exact room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
            }
        )

    def chat_message(self, event):
        # send only to sockets in this same room_group_name
        self.send_json({
            "message": event["message"]
        })
