from django.contrib import admin
HOST = "127.0.0.1"
PORT = 8080
def shutdown_cam_feed_server():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'shutDown')

# Register your models here.
