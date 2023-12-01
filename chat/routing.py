from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/socket-server/c/<str:pk>", consumers.ChatConsumer.as_asgi()),
]
