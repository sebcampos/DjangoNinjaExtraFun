from django.test import TestCase
import socket, cv2
import numpy as np

HOST = "127.0.0.1"
PORT = 8080


# Create your tests here.
def test_local_camera_stream():
    count = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'connect')
        while count < 100:
            size_m = s.recv(1024)
            size = int(size_m.split()[-1])
            s.sendall(b'received frame size')
            frame = b""
            while len(frame) < size:
                frame += s.recv(size)
            image = cv2.imdecode(np.asarray(bytearray(frame)), -1)
            image = cv2.resize(image, (5000, 5000))
            cv2.imshow("image", image)
            count += 1
            if count != 100:
                s.sendall(b'received frame')
        s.sendall(b'close')
        cv2.destroyAllWindows()


if __name__ == '__main__':
    test_local_camera_stream()
"incremental, txaio, setuptools, pycparser, pyasn1, idna, constantly, attrs, zope-interface, pyasn1-modules, hyperlink, channels, cffi, automat, twisted, cryptography, service-identity, pyopenssl, autobahn, daphne"