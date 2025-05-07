from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        print("WebSocket: CONNECTED")
        await self.accept()

    async def receive(self, text_data):
        print(f"WebSocket: RECEIVED message {text_data}")
        self.send(text_data="Hello world!")

    async def disconnect(self, close_code):
        print(f"WebSocket: DISCONNECTED with code {close_code}")