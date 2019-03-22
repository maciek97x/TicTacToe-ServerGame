# -*- coding: utf-8 -*-

import socket
import sys
import traceback
from threading import Thread
import os
from random import randint
import re

os.system("mode con: cols=50 lines=20")
players = dict([])
game_in_progress = False
board = [[0 for _ in range(3)] for _ in range(3)]
players['none'] = 'none'
player_x = 'none'
player_o = 'none'
player_move = 1
send_state = dict([])

def save_to_file(msg, ip, port, if_out):
    file = open('server_log.txt', 'a')
    if if_out:
        file.write('to   {}:{} '.format(ip, port))
    else:
        file.write('from {}:{} '.format(ip, port))
    file.write(msg + '\n')
    file.close()

def check_board():
    global board
    # <----- to do

def start_server():
    host = "127.0.0.1"
    port = 8888  # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)  # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with {}:{}".format(ip, port))

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
            Thread(target=data_receive_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
    soc.close()
    
def data_receive_thread(connection, ip, port, max_buffer_size=5120):
    global board
    global game_in_progress
    global players
    global player_x
    global player_o
    global player_move
    player_id = '{}:{}'.format(ip, port)

    # game loop
    while True:
        received_data = connection.recv(max_buffer_size).decode('utf8')
        print('received: {}'.format(received_data))
        data = received_data.split()
        if not game_in_progress:
            if re.match(r'^sit_x', received_data):
                if player_x == 'none':
                    player_x = player_id
                    players[player_id][1] = 1
                    # send update for all clients
                    for key in send_state.keys():
                        send_state[key] = True
            if re.match(r'^sit_o', received_data):
                if player_o == 'none':
                    player_o = player_id
                    players[player_id][1] = 2
                    for key in send_state.keys():
                        send_state[key] = True
            if player_o != 'none' and player_x != 'none':
                # init game
                game_in_progress = True
                player_move = 1
                board = [[0 for _ in range(3)] for _ in range(3)]
                
        else:
            print(player_move, data[1:3], players[player_id][1])
            if player_move == players[player_id][1] and re.match('^move [0-2] [0-2]', received_data) is not None:
                x, y = map(int, data[1:3])
                if board[x][y] == 0:
                    board[x][y] = players[player_id][1]
                    player_move = 3 - player_move
                    for key in send_state.keys():
                        send_state[key] = True
            

def client_thread(connection, ip, port, max_buffer_size=5120):
    global board
    global game_in_progress
    global players
    global player_x
    global player_o
    global player_move

    player_nickname = connection.recv(max_buffer_size).decode('utf8')
    player_id = 1
    player_mode = 0
    
    player_id = '{}:{}'.format(ip, port)
    players[player_id] = [player_nickname, 0]
    send_state[player_id] = False
    
    for key in send_state.keys():
        send_state[key] = True
    
    while True:
        # send game state to client if need to
        if send_state[player_id]:
            game_state = 'p ' + ' '.join([players[x][0] for x in players.keys() if x != 'none']) +\
                        ' b ' + ' '.join(map(str, [board[x//3][x%3] for x in range(9)])) +\
                        ' x ' + str(players[player_x][0]) +\
                        ' o ' + str(players[player_o][0]) +\
                        ' m ' + str(int(player_move == players[player_id][1]))
            connection.send(game_state.encode('utf8'))
            send_state[player_id] = False
        
start_server()
