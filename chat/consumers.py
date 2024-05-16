from typing import List

from channels.generic.websocket import JsonWebsocketConsumer
from .models import RolePlayingRoom, GptMessage


"""
WSGI : ASGI ~= views.py : consumers.py

<views.py>              <consumers.py>
request.user          self.scope['user']
URL Captured Value    self.scope['url_route']
"""


# 대화내역 - 채팅방에 접속되어 있는 동안에만 유지되도 충분 -> Consumer 인스턴스 내에서 인스턴스 변수에 저장
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_msg: List[GptMessage] = []

    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            self.gpt_msg = room.get_initial_messages()
            print(self.gpt_msg)

    def receive_json(self, content, **kwargs):
        print("received:", content)
        # json 역직렬화
        # Echo
        self.send_json(content)

    def get_room(self):
        user = self.scope["user"]
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        room: RolePlayingRoom = None

        if user.is_authenticated:
            try:
                room = RolePlayingRoom.objects.get(pk=room_pk, user=user)
            except RolePlayingRoom.DoesNotExist:
                pass

        return room
