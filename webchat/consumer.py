from channels.generic.websocket import WebsocketConsumer


class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        # Accept connection with no subprotocol
        self.accept()
        print("WebSocket request headers:", self.scope.get("headers"))

    def receive(self, text_data=None, bytes_data=None):
        # Echo the received text data back to the client
        if text_data:
            self.send(text_data=f"Received: {text_data}")
        elif bytes_data:
            self.send(bytes_data=bytes_data)

    def disconnect(self, close_code):
        # Handle disconnection logic here
        pass
