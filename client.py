import socket
import sys
import time
import pygame
from pygame.locals import *
from threading import Thread
from mygui import *


import os

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888


# window size
window_width = 900
window_height = 700
graph_size = 600

# initializing window
pygame.init()
window = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Interpolacja wielomianem i splajnem')
icon = pygame.Surface((1, 1))
icon.fill((255, 255, 255))
pygame.display.set_icon(icon)


def handle_connection(socket):
    while True:
        msg_from_server = socket.recv(1024).decode("utf8")
        

try:
    soc.connect((host, port))
except:
    print("Connection error")
    sys.exit()


# main loop
while True:
    # handling events
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

