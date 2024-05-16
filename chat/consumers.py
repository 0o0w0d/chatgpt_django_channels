from channels.generic.websocket import JsonWebsocketConsumer


class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def receive_json(self, content, **kwargs):
        print("received:", content)
        # json 역직렬화
        # Echo
        self.send_json(content)
