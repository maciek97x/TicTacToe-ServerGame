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
if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = 'localhost'
print('host: {}'.format(host))
port = 8888

# window size
window_width = 600
window_height = 400

# initializing window
pygame.init()
window = pygame.display.set_mode((window_width, window_height), 0, 32)
pygame.display.set_caption('Tic Tac Toe')
icon = pygame.Surface((1, 1))
icon.fill((255, 255, 255))
pygame.display.set_icon(icon)

# game state variables
login = ''
password = ''
login_success = 0
board = [[0 for x in range(3)] for y in range(3)]
players_list = []
player_x = ''
player_o = ''
player_move = 0
player_win = 0
my_move = True


def terminate():
    global soc
    soc.send('quit'.encode('utf8'))
    time.sleep(.5)
    soc.close()
    pygame.quit()
    sys.exit()
    
def connection_thread():
    global gui
    global board
    global players_list
    global player_x
    global player_o
    global player_win
    global soc
    global login
    global password
    global login_success
    global my_move
    
    print('thread started')
    
    if menu == 'try_login':
        soc.send('login {} {}'.format(login, password).encode('utf8'))
        print('sending: login {} {}'.format(login, password))
    else:
        soc.send('register {} {}'.format(login, password).encode('utf8'))
        print('sending: register {} {}'.format(login, password))
    login_result = soc.recv(1024).decode('utf8')
    if re.match(r'success', login_result) is not None:
        print('login success')
        login_success = 1
    else:
        print('login error')
        login_success = 2
        return
        
    while True:
        # receive game state from server
        print('waiting for data')
        msg_from_server = soc.recv(1024).decode('utf8')
        if re.match(r'^closed', msg_from_server) is not None:
            break
        # decode data
        received_data = msg_from_server.split()
        print('received: {}'.format(received_data))
        p_index = received_data.index('p')
        b_index = received_data.index('b')
        x_index = received_data.index('x')
        o_index = received_data.index('o')
        n_index = received_data.index('n')
        w_index = received_data.index('w')
        m_index = received_data.index('m')
        for x in range(3):
            for y in range(3):
                board[x][y] = int(received_data[b_index + 1 + 3*x + y])
                if gui.id_exists('button_board_{}_{}'.format(x, y)):
                    gui.get_element('button_board_{}_{}'.format(x, y)).text = ' OX'[board[x][y]]
        players_list = received_data[p_index + 1:b_index]
        player_x = received_data[x_index + 1]
        player_o = received_data[o_index + 1]
        player_move = int(received_data[n_index + 1])
        player_win = int(received_data[w_index + 1])
        my_move = bool(int(received_data[m_index + 1]))
        if gui.id_exists('textlist_players'):
            gui.get_element('textlist_players').text_list = players_list
        if gui.id_exists('text_player_o'):
            gui.get_element('text_player_o').text = ' > '[player_move]
        if gui.id_exists('button_o'):
            gui.get_element('button_o').text = player_o
        if gui.id_exists('text_player_x'):
            gui.get_element('text_player_x').text = '  >'[player_move]
        if gui.id_exists('button_x'):
            gui.get_element('button_x').text = player_x
        if gui.id_exists('text_player_win'):
            if player_win == 0:
                gui.get_element('text_player_win').text = ''
            elif player_win == 3:
                gui.get_element('text_player_win').text = 'no one wins'
            else:
                gui.get_element('text_player_win').text = '{} wins'.format(' OX'[player_win])
            
def set_menu(value):
    global menu
    menu = value

def sit(value):
    if value in 'xo':
        if (value == 'x' and player_x == 'none') or (value == 'o' and player_o == 'none'):
            print('sending: sit_{}'.format(value))
            soc.send('sit_{} '.format(value).encode('utf8'))

def send_move(x, y):
    global my_move
    if my_move:
        if board[x][y] == 0:
            my_move = False
        print('sending: move {} {}'.format(x, y))
        soc.send('move {} {} '.format(x, y).encode('utf8'))

menu = 'login'

gui = mygui.GUI(window)

# main loop
while True:
    # connection menu
    if menu == 'login':
        # gui
        login_success = 0
        gui.clear()
        gui.add('textbox_login', mygui.TextBox(window, (180, 100), (240, 40),\
                                                  'login'))
        gui.add('textbox_password', mygui.TextBox(window, (180, 180), (240, 40),\
                                                  'password'))
        gui.add('login_button', mygui.Button(window, (180, 260), (100, 40),\
                                               'login', on_action=set_menu,\
                                               on_action_args=('try_login',)))
        gui.add('register_button', mygui.Button(window, (320, 260), (100, 40),\
                                               'register', on_action=set_menu,\
                                               on_action_args=('register',)))
        gui.get_element('textbox_login').text = login
    while menu == 'login':
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
        
    if menu in ['try_login', 'register']:
        # connection with server
        connected = True
        login = gui.get_element('textbox_login').text
        password = gui.get_element('textbox_password').text # <--hash it
        if len(login) < 4 or len(password) < 4:
            print('too short login or password')
            menu = 'login'
        else:
            try:
                print('trying to connect')
                soc.connect((host, port))
                print('trying to start thread')
                Thread(target=connection_thread).start()
            except:
                connected = False
            if connected:
                while login_success == 0:
                    pass
            gui.clear()
            if not connected:
                gui.add('textbox_connection_error', mygui.Text(window, (180, 140), (240, 40),\
                                                               'Connection error'))
                gui.add('button_retry', mygui.Button(window, (180, 220), (240, 40), 'Retry connection',\
                                                     on_action=set_menu, on_action_args=('login',)))
            elif login_success != 1:
                gui.add('textbox_connection_error', mygui.Text(window, (180, 140), (240, 40),\
                                                               'Login error'))
                gui.add('button_retry', mygui.Button(window, (180, 220), (240, 40), 'Retry',\
                                                     on_action=set_menu, on_action_args=('login',)))
                soc.close()
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                gui.add('textbox_connected', mygui.Text(window, (180, 140), (240, 40),\
                                                        'Connected with server'))
                gui.add('textbox_ok', mygui.Button(window, (180, 220), (240, 40), 'OK',\
                                               on_action=set_menu, on_action_args=('game',)))
    while menu in ['try_login', 'register']:
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
    # game
    if menu == 'game':
        gui.clear()
        for x in range(3):
            for y in range(3):
                gui.add('button_board_{}_{}'.format(x, y),\
                        mygui.Button(window, (30 + 120*x, 30 + 120*y), (100, 100),\
                                     on_action=send_move, on_action_args=(x, y)))
        gui.add('textlist_players', mygui.TextList(window, (510, 20), (80, 20), ['xxx']))
        gui.add('text_player_x', mygui.Text(window, (370, 50), (40, 40)))
        gui.add('button_x', mygui.Button(window, (410, 60), (80, 20),\
                                         on_action=sit, on_action_args=('x')))
        gui.add('text_player_o', mygui.Text(window, (370, 110), (40, 40)))
        gui.add('button_o', mygui.Button(window, (410, 120), (80, 20),\
                                         on_action=sit, on_action_args=('o')))
        gui.add('text_player_win', mygui.Text(window, (510, 300), (80, 20)))
        
    while menu == 'game':
        # handling events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            gui.handle_event(event)
            
        window.fill(mygui.colors['white'])
        gui.draw()
        pygame.display.update()
















