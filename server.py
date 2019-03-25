# -*- coding: utf-8 -*-

import hashlib
import binascii
import socket
import sys
import traceback
from threading import Thread
import os
from random import randint
import re
import time

os.system("mode con: cols=50 lines=20")
players = dict([])
game_in_progress = False
board = [[0 for _ in range(3)] for _ in range(3)]
players['none'] = ['none', 0, 0]
player_x = 'none'
player_o = 'none'
player_win = 0
player_move = 1
send_state = dict([])

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf8'),\
                                        salt, 100000)
    password_hash = binascii.hexlify(password_hash)
    return (salt + password_hash).decode('ascii')

def verify_password(stored, provided):
    salt = stored[:64]
    stored = stored[64:]
    password_hash = hashlib.pbkdf2_hmac('sha512', provided.encode('utf8'),\
                                        salt.encode('ascii'), 100000)
    password_hash = binascii.hexlify(password_hash).decode('ascii')
    return stored == password_hash

def save_to_file(msg, ip, port, if_out):
    file = open('server_log.txt', 'a')
    if if_out:
        file.write('to   {}:{} {}\n'.format(ip, port, msg))
    else:
        file.write('from {}:{} {}\n'.format(ip, port, msg))
    file.close()

def check_board():
    global board
    sums = [[0, 0] for _ in range(8)]
    empty = 0
    for x in range(3):
        for y in range(3):
            if board[x][y] != 0:
                sums[x][board[x][y] - 1] += 1
                sums[3 + y][board[x][y] - 1] += 1
                if x == y:
                    sums[6][board[x][y] - 1] += 1
                if x == 2 - y:
                    sums[7][board[x][y] - 1] += 1
            else:
                empty += 1
    for o, x in sums:
        if o == 3:
            return 1
        elif x == 3:
            return 2
    if empty == 0:
        return 3
    return 0

def start_server():
    host = 'localhost'
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
        print('waiting for connection')
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with {}:{}".format(ip, port))
        action, player_nickname, player_password = connection.recv(5120).decode('utf8').split()[0:3]
        print('received: {} {} {} from {}:{}'.format(action, player_nickname, player_password, ip, port))
        login_ok = False
        player_points = 0
        if action == 'login':
            login_ok = False
            for line in open('users.txt', 'r').readlines():
                line = line.split()
                if player_nickname == line[0] and\
                   verify_password(line[1], player_password):
                    login_ok = True
                    player_points = int(line[2])
                    break
        elif action == 'register':
            login_ok = True
            for line in open('users.txt', 'r').readlines()[:-1]:
                line = line.split()
                if player_nickname == line[0]:
                    login_ok = False
                    break
            if login_ok:
                file_users = open('users.txt', 'a')
                file_users.write('{} {} {}\n'.format(player_nickname, hash_password(player_password), 0))
                file_users.close()

        if  not login_ok:
            connection.send('failure'.encode('utf8'))
        else:
            connection.send('success'.encode('utf8'))
            
            player_id = '{}:{}'.format(ip, port)
            players[player_id] = [player_nickname, 0, player_points]
            send_state[player_id] = True
            
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
    global player_win
    global player_move
    player_id = '{}:{}'.format(ip, port)
    
    time.sleep(1)

    # game loop
    while True:
        received_data = connection.recv(max_buffer_size).decode('utf8')
        print('received: {} from {}:{}'.format(received_data, ip, port))
        data = received_data.split()
        if re.match(r'^quit', received_data ) is not None:
            del players[player_id]
            del send_state[player_id]
            if player_o == player_id:
                player_o = 'none'
                game_in_progress = False
            if player_x == player_id:
                player_x = 'none'
                game_in_progress = False
            connection.send('closed'.encode('utf8'))
            for key in send_state.keys():
                send_state[key] = True            
            break
        
        if not game_in_progress:
            if re.match(r'^sit_o', received_data):
                if player_o == 'none' and player_x != player_id:
                    player_o = player_id
                    players[player_id][1] = 1
                    for key in send_state.keys():
                        send_state[key] = True
            if re.match(r'^sit_x', received_data):
                if player_x == 'none' and player_o != player_id:
                    player_x = player_id
                    players[player_id][1] = 2
                    # send update for all clients
                    for key in send_state.keys():
                        send_state[key] = True
            if player_o != 'none' and player_x != 'none':
                # init game
                game_in_progress = True
                player_move = randint(1,2)
                player_win = 0
                board = [[0 for _ in range(3)] for _ in range(3)]
                
        else:
            if player_move == players[player_id][1] and re.match('^move [0-2] [0-2]', received_data) is not None:
                x, y = map(int, data[1:3])
                if board[x][y] == 0:
                    board[x][y] = players[player_id][1]
                    player_move = 3 - player_move
                    win = check_board()
                    if win != 0:
                        player_x = 'none'
                        player_o = 'none'
                        player_win = win                    
                        for key in players.keys():
                            if players[key][1] == win:
                                players[key][2] += 1
                            elif players[key][1] == 3 - win:
                                players[key][2] -= 1
                        game_in_progress = False
                    for key in send_state.keys():
                        send_state[key] = True
                    
            

def client_thread(connection, ip, port, max_buffer_size=5120):
    global board
    global game_in_progress
    global players
    global player_x
    global player_o
    global player_win
    global player_move
    
    player_id = '{}:{}'.format(ip, port)
    player_nickname = players[player_id]
    
    for key in send_state.keys():
        send_state[key] = True
        
    time.sleep(1)
    while True:
        # send game state to client if need to
        try:
            if send_state[player_id]:
                game_state = 'p ' + ' '.join([players[x][0] + '_' + str(players[x][2])\
                                              for x in players.keys() if x != 'none']) +\
                            ' b ' + ' '.join(map(str, [board[x//3][x%3] for x in range(9)])) +\
                            ' x ' + str(players[player_x][0]) +\
                            ' o ' + str(players[player_o][0]) +\
                            ' n ' + str(player_move) +\
                            ' w ' + str(player_win) +\
                            ' m ' + str(int(player_move == players[player_id][1]))
                connection.send(game_state.encode('utf8'))
                send_state[player_id] = False
        except:
            break
start_server()
