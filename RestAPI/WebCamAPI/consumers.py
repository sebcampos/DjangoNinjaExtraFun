import json
from channels.generic.websocket import WebsocketConsumer

class VideoConsumer(WebsocketConsumer):
    def connect(self):
        # connect to the video stream
        self.accept()

    def disconnect(self, close_code):
        # disconnect from the video stream
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the received message to all clients
        self.send(text_data=json.dumps({
            'message': message
        }))