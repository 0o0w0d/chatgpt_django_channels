from django.urls import re_path, path
from . import consumers

# WSGI : ASGI ~= urls.py : routing.py


websocket_urlpatterns = [
    path("ws/chat/<int:room_pk>/", consumers.RolePlayingRoomConsumer.as_asgi())
]
