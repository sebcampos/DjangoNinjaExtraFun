import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # connection from client add to cam `group`
        await self.channel_layer.group_add("cam", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # disconnect from the video stream, remove from cam group
        await self.channel_layer.group_discard("cam", self.channel_name)

    async def receive(self, text_data):
        # receive a message from cam
        print("received text: " + text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Broadcast the received message to all clients
        await self.channel_layer.group_send(
            "cam",
            {
                "type": "chat.message",
                "message": message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # this method maps to the chat.message type, invoked by broadcasted channel_layer.groupsend
        message = event["message"]

        print("CHATMESSAGE")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))