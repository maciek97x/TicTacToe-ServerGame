import socket
import sys
import time
from threading import Thread

import os

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888

try:
    soc.connect((host, port))
except:
    print("Connection error")
    sys.exit()

while True:
    msg_from_server = soc.recv(1024).decode("utf8")
    print(msg_from_server, end='')
    if 'TWOJ RUCH' in msg_from_server:
        # timeout
        message = input()
        soc.sendall(message.encode("utf8"))
    if 'POLACZONO' in msg_from_server:
        message = input()
        soc.sendall(message.encode("utf8"))
        

soc.send(b'--quit--')
