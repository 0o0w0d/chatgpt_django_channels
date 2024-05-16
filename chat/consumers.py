from typing import List

import openai

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
        self.gpt_msgs: List[GptMessage] = []
        self.recommend_msg = ""

    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            self.gpt_msgs = room.get_initial_messages()
            self.recommend_msg = room.get_recommend_message()

            assistant_msg = self.gpt_query()
            # 초기 프롬프트가 적용된 gpt 응답 전달
            self.send_json({"type": "assistant-msg", "message": assistant_msg})

    def receive_json(self, content: dict, **kwargs):
        # user-msg 타입으로 json 파일을 받으면, assistant-msg 타입으로 gpt response 전달
        if content["type"] == "user-msg":
            assistant_msg = self.gpt_query(user_query=content["message"])
            self.send_json({"type": "assistant-msg", "message": assistant_msg})
        elif content["type"] == "request-recommend-msg":
            recommend_msg = self.gpt_query(command_query=self.recommend_msg)
            self.send_json({"type": "recommended-msg", "message": recommend_msg})

        # 그 외의 타입일 경우 invalid type message
        else:
            self.send_json(
                {"type": "error", "message": f"Invalid type: {content['type']}"}
            )

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

    # user 메시지에 대한 gpt 응답을 반환하는 메소드
    def gpt_query(self, command_query: str = None, user_query: str = None) -> str:
        """
        user_query: 사용자의 대화 메시지
        command_query: 표현 추천 등의 요청
        두 인자는 배타적 관계
        """

        # user가 보낸 메시지
        if command_query is not None and user_query is not None:
            raise ValueError("Can't use command_query, user_query together")
        elif command_query is not None:  # command_query 값이 있으면
            self.gpt_msgs.append(GptMessage(role="user", content=command_query))
        elif user_query is not None:  # user_query 값이 있으면
            self.gpt_msgs.append(GptMessage(role="user", content=user_query))

        # gpt 응답 생성
        response_dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.gpt_msgs, temperature=1
        )
        response_role = response_dict["choices"][0]["message"]["role"]
        response_content = response_dict["choices"][0]["message"]["content"]

        # gpt가 보낸 메시지
        if command_query is None:
            # websocket이 연결되어 있는 동안, command_query가 아닐 경우 대화내역 저장
            gpt_msg = GptMessage(role=response_role, content=response_content)
            self.gpt_msgs.append(gpt_msg)

        return response_content
