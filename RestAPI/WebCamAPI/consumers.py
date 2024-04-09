import json
from channels.generic.websocket import AsyncWebsocketConsumer
import socket
import asyncio
from time import sleep

HOST = "127.0.0.1"
PORT = 8080


class ChatConsumer(AsyncWebsocketConsumer):
    group_name = 'chat'

    async def connect(self):
        # connection from client add to cam `group`
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # disconnect from the video stream, remove from cam group
        print("disconnect sent code to chat", close_code)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        content = text_data_json['content']
        if message_type == "update":
            print("update received")
            print("update lists")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(b"new_list_packet")

            # Broadcast the received message to all clients
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "video.update",
                    "message": content
                }
            )

        elif message_type == "chat":
            print("chat message revieced")
            # Broadcast the received message to all clients
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": content
                }
            )


    async def chat_message(self, event):
        # this method maps to the chat.message type, invoked by broadcasted channel_layer.groupsend
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class VideoConsumer(AsyncWebsocketConsumer):
    group_name = 'cam'
    cam_sock_connection: socket.socket

    async def collect_frame(self):
        size_m = self.cam_sock_connection.recv(1024)
        size = int(size_m.split()[-1])
        self.cam_sock_connection.sendall(b'received frame size')
        frame = b""
        while len(frame) < size:
            frame += self.cam_sock_connection.recv(size)
        self.cam_sock_connection.sendall(b'received frame')
        return frame

    async def connect(self):
        # connection from client add to cam `group`
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.cam_sock_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cam_sock_connection.connect((HOST, PORT))
        self.cam_sock_connection.sendall(b'connect')

    async def disconnect(self, close_code):
        # disconnect from the video stream, remove from cam group
        print("disconnect sent code to vidcam", close_code)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        frame = await self.collect_frame()
        await self.send(bytes_data=frame)

