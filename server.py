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
player_move = 0
send_state = dict([])

def save_to_file(msg, ip, port, if_out):
    file = open('server_log.txt', 'a')
    if if_out:
        file.write('to   {}:{} '.format(ip, port))
    else:
        file.write('from {}:{} '.format(ip, port))
    file.write(msg + '\n')
    file.close()

def next_player(current_id, id_list):
    new_list = list(filter(lambda x: x > current_id, id_list))
    if len(new_list) > 0:
        return new_list[0]
    else:
        return id_list[0]
    
def if_new_round(current_id, first_id, id_list):
    if current_id == first_id:
        return True
    i = 0
    while id_list[i] < first_id:
        i += 1
    
    if id_list[i%len(id_list)] == current_id:
        return True
    return False

def show_board():
    global board
    for x in range(5):
        for y in range(5):
            print(board[y][x], end='')
        print('')
    print('')

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
    while player_id in players.keys():
        player_id += 1
    players[player_id] = player_nickname
    send_state[player_id] = False
    game_in_progress = False

    while not game_in_progress:
        pass

    if game_in_progress:
        board = [[0 for _ in range(3)] for _ in range(3)]
    while game_in_progress:
        game_state = ''
        game_state += 'p ' + ' '.join([players[x] for x in players.keys() if x != -1])
        game_state += ' b ' + ' '.join(map(str, [board[x//3][x%3] for x in range(9)]))
        game_state += ' x ' + str(players[player_x])
        game_state += ' o ' + str(players[player_o])
        game_state += ' m ' + str(int(player_move == player_id))
        connection.send(game_state.encode('utf8'))
        print(receive_input(connection, ip, port, max_buffer_size))

def receive_input(connection, ip, port, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line

    return decoded_input


start_server()
