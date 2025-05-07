from django.urls import path

from webchat.consumer import MyConsumer

websocket_urlpatterns = [
    path("ws/test/", MyConsumer.as_asgi()),
]