from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/video/live', consumers.VideoConsumer.as_asgi()),
    re_path('ws/video/chat', consumers.ChatConsumer.as_asgi())
]
