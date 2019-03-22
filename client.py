import socket
import sys
import time
import pygame
from pygame.locals import *
from threading import Thread
import mygui
import re


import os

# creating socket
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888

# window size
window_width = 400
window_height = 400

# initializing window
pygame.init()
window = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Tic Tac Toe')
icon = pygame.Surface((1, 1))
icon.fill((255, 255, 255))
pygame.display.set_icon(icon)

# game state variables
nickname = ''
board = [[0 for x in range(3)] for y in range(3)]
players_list = []
player_x = ''
player_o = ''
my_move = True


def terminate():
    global soc
    soc.close()
    pygame.quit()
    sys.exit()
    
def connection_thread():
    global gui
    global board
    global players_list
    global player_x
    global player_o
    global soc
    global nickname
    global my_move
    
    soc.send(nickname.encode('utf8'))
    
    while True:
        # receive game state from server
        msg_from_server = soc.recv(1024).decode('utf8')
        # decode data
        print(msg_from_server)
        received_data = msg_from_server.split()
        print('received: {}'.format(received_data))
        p_index = received_data.index('p')
        b_index = received_data.index('b')
        x_index = received_data.index('x')
        o_index = received_data.index('o')
        m_index = received_data.index('m')
        for x in range(3):
            for y in range(3):
                board[x][y] = int(received_data[b_index + 1 + 3*x + y])
                if gui.id_exists('button_board_{}_{}'.format(x, y)):
                    gui.get_element('button_board_{}_{}'.format(x, y)).text = ' OX'[board[x][y]]
        players_list = received_data[p_index + 1:b_index]
        player_x = received_data[x_index + 1]
        player_o = received_data[o_index + 1]
        my_move = bool(int(received_data[m_index + 1]))
        if gui.id_exists('textlist_players'):
            gui.get_element('textlist_players').text_list = players_list
        if gui.id_exists('button_o'):
            gui.get_element('button_o').text = player_o
        if gui.id_exists('button_x'):
            gui.get_element('button_x').text = player_x
        
def next_menu():
    global menu
    menu += 1
        
def set_menu(value):
    global menu
    menu = value

def sit(value):
    if value in 'xo':
        print('sending: sit_{}'.format(value))
        soc.send('sit_{}'.format(value).encode('utf8'))

def click_board(x, y):
    global my_move
    if my_move:
        print('sending: move {} {}'.format(x, y))
        soc.send('move {} {}'.format(x, y).encode('utf8'))
        my_move = False

menu = 0

gui = mygui.GUI(window)

# main loop
while True:
    # connection menu
    if menu == 0:
        # gui
        gui.clear()
        gui.add('textbox_nickname', mygui.TextBox(window, (60, 60), (100, 20), 'insert your nick'))
        gui.add('connect_button', mygui.Button(window, (60, 100), (100, 20), 'connect', on_action=next_menu))
    while menu == 0:
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
    # connection result
    if menu == 1:
        # connection with server
        connected = True
        nickname = gui.get_element('textbox_nickname').text
        try:
            soc.connect((host, port))
            Thread(target=connection_thread).start()
        except:
            connected = False
        gui.clear()
        if connected:
            gui.add('textbox_connected', mygui.Text(window, (60, 60), (100, 20), 'Connected with server'))
            gui.add('textbox_ok', mygui.Button(window, (60, 100), (100, 20), 'OK', on_action=next_menu))
        else:
            gui.add('textbox_connection_error', mygui.Text(window, (60, 60), (100, 20), 'Connection error'))
            gui.add('button_retry', mygui.Button(window, (60, 100), (100, 20), 'Retry connection', on_action=set_menu, on_action_args=(0,)))
    while menu == 1:
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
    # game
    if menu == 2:
        gui.clear()
        for x in range(3):
            for y in range(3):
                gui.add('button_board_{}_{}'.format(x, y),\
                        mygui.Button(window, (50 + 50*x, 50 + 50*y), (40, 40),\
                                     on_action=click_board, on_action_args=(x, y)))
        gui.add('textlist_players', mygui.TextList(window, (300, 20), (100,20), ['xxx']))
        gui.add('button_x', mygui.Button(window, (10, 110), (40, 20),\
                                         on_action=sit, on_action_args=('x')))
        gui.add('button_o', mygui.Button(window, (200, 110), (40, 20),\
                                         on_action=sit, on_action_args=('o')))
        
    while menu == 2:
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
















