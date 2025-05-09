from django.urls import path

from webchat import consumer

websocket_urlpatterns = [
    path('<str:serverId>/<str:channelId>', consumer.ChatConsumer.as_asgi()),
]