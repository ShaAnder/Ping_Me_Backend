from django.urls import path

from webchat import consumer

websocket_urlpatterns = [
    path('ws/chat/test/', consumer.ChatConsumer.as_asgi()),
]