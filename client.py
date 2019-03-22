import socket
import sys
import time
import pygame
from pygame.locals import *
from threading import Thread
import mygui


import os

# creating socket
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
pygame.display.set_caption('Tic Tac Toe')
icon = pygame.Surface((1, 1))
icon.fill((255, 255, 255))
pygame.display.set_icon(icon)


def terminate():
    pygame.quit()
    sys.exit()
    
def handle_connection(socket):
    while True:
        msg_from_server = socket.recv(1024).decode("utf8")
        
'''
try:
    soc.connect((host, port))
except:
    print("Connection error")
    sys.exit()
'''
        
menu = 0

gui = mygui.GUI(window)
gui.add(mygui.TextBox(window, (60, 60), (100, 20), 'insert your nick'))

# main loop
while True:
    if menu == 0:
        while True:
            # handling events
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                gui.handle_event(event)
                
            window.fill(mygui.colors['white'])
            gui.draw()
            pygame.display.update()
