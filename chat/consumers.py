from channels.generic.websocket import JsonWebsocketConsumer


# 대화내역 - 채팅방에 접속되어 있는 동안에만 유지되도 충분 -> Consumer 인스턴스 내에서 인스턴스 변수에 저장
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    def receive_json(self, content, **kwargs):
        # receive 할 때 마다 count +1
        self.count += 1
        content["count"] = self.count
        print("received:", content)
        # json 역직렬화
        # Echo
        self.send_json(content)
