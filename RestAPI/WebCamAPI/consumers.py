import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected')
        # connect to the video stream
        self.accept()

    async def disconnect(self, close_code):
        # disconnect from the video stream
        print('disconnected')
        pass

    async def receive(self, text_data):
        print("received text: " + text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the received message to all clients
        self.send(text_data=json.dumps({
            'message': message
        }))