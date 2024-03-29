import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected')
        # connect to the video stream
        await self.channel_layer.group_add("cam", "live")
        await self.accept()

    async def disconnect(self, close_code):
        # disconnect from the video stream
        print('disconnected')

        await self.channel_layer.group_discard("cam", "live")

    async def receive(self, text_data):
        print("received text: " + text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the received message to all clients
        await self.send(text_data=json.dumps({
            'message': message
        }))