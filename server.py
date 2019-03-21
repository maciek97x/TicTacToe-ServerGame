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
active_player = -1
first_player = -1
game_in_progress = False
init_game = dict([])
send_attack_result = dict([])
send_round_end = dict([])
send_game_over = dict([])
attack_result = ''
board = [[[0, 0] for _ in range(5)] for _ in range(5)]
round_count = 0
season_count = 0
season_results = [[] for _ in range(10)]
active_id = []

def save_to_file(msg, ip, port, if_out):
    file = open('communication.txt', 'a')
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
    pass

def receive_input(connection, ip, port, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = decoded_input.upper()
    save_to_file(result, ip, port, 0)

    return result


start_server()