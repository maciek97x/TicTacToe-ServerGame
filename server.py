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
player_x = -1
player_o = -1
players[-1] = 'none'
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

def check_board()
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
        connection.send('POLACZONO\n'.encode('utf8'))
        save_to_file('POLACZONO', ip, port, 1)
        print("Connected with {}:{}".format(ip, port))

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()

def client_thread(connection, ip, port, max_buffer_size=5120):
    global board
    global game_in_progress
    global players
    global player_x
    global player_o
    global player_move

    player_nickname = receive_input(connection, ip, port, max_buffer_size)
    player_id = 1
    player_mode = 0

    while player_id in players.keys():
        player_id += 1
    players[player_id] = player_nickname
    send_state[player_id] = False
    game_in_progress = False

    while True:

        # wait for two players to choose x and o
        while not game_in_progress:
            # send game state to client if need to
            if send_state[player_id]:
                game_state = ''
                game_state += 'p ' + ' '.join([players[x] for x in players.keys() if x != -1])
                game_state += ' b ' + ' '.join(map(str, [board[x//3][x%3] for x in range(9)]))
                game_state += ' x ' + str(players[player_x])
                game_state += ' o ' + str(players[player_o])
                game_state += ' m ' + str(int(player_move == player_id))
                connection.send(game_state.encode('utf8'))
            # receive data from client
            received_data = receive_input(connection, ip, port, max_buffer_size)
            if re.match(r'sit_x', received_data):
                if player_x == -1:
                    player_x = player_id
                    player_mode = 1
                    # send update for all clients
                    for key in send_state.keys():
                        send_state[key] = True
            if re.match(r'sit_o', received_data):
                if player_o == -1:
                    player_o = player_id
                    player_mode = 2
                    for key in send_state.keys():
                        send_state[key] = True
            if player_o != -1 and player_x != -1:
                game_in_progress = True
        # init game
        if game_in_progress:
            board = [[0 for _ in range(3)] for _ in range(3)]
        # game loop
        while game_in_progress:
            if send_state[player_id]:
                game_state = ''
                game_state += 'p ' + ' '.join([players[x] for x in players.keys() if x != -1])
                game_state += ' b ' + ' '.join(map(str, [board[x//3][x%3] for x in range(9)]))
                game_state += ' x ' + str(players[player_x])
                game_state += ' o ' + str(players[player_o])
                game_state += ' m ' + str(int(player_move == player_id))
                connection.send(game_state.encode('utf8'))
            received_data = receive_input(connection, ip, port, max_buffer_size)
            # if player is x or o
            if player_mode != 0:
                # if its his move and he send correct data
                if player_move == player_mode and re.match(r'move [0-2] [0-2]', received_data):
                    x, y = map(int, received_data[1:3])
                    # if move is possible
                    if board[x][y] == 0:
                        board[x][y] = player_mode
                        player_move = 3 - player_move
                        win = check_board()
                        if win != 0:
                            game_in_progress = False
                        for key in send_state.keys():
                            send_state[key] = True

def receive_input(connection, ip, port, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line

    return decoded_input


start_server()
