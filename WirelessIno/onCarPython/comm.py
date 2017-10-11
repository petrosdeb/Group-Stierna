'''
    Simple socket server using threads
'''

import socket
import sys
from _thread import start_new_thread
import os


# opens a socket and starts a thread listening for communication on that socket
def start_listen(port, host=''):
    data_log = []  # each thread writes to the same array (which might be a bad idea)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Socket created: \'' + host + '\'@' + str(port))

    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
        sys.exit()

    print('Socket bind complete')
    s.listen(10)

    print('Socket now listening')

    start_new_thread(listen_thread, (s, data_log))

    return data_log


# thread listening for socket communication
def listen_thread(s, data_log):
    while True:
        conn, address = s.accept()
        # print('Connected with ' + address[0] + ':' + str(address[1]))

        # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(client_thread, (conn, data_log, address))


# a new client_thread is opened whenever a new connection is established
def client_thread(conn, data_log, address):
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        raw_data = conn.recv(1024)

        if not raw_data:
            break

        # Skip the surrounding junk
        data = raw_data.decode("utf-8").rstrip()

        data_log.append(data)
        # print(data_log)

        interpret(data)

    # came out of loop
    conn.close()  # now keep talking with the client
    #  print('Connection closed: ' + address[0] + ':' + str(address[1]))


# decides what to do with a received message
def interpret(data):
    if not data:
        return
    args = data.split(" ")

    fun = args[0]
    val = args[1]

    if fun == 'a':
        do_acc(val)
    elif fun == 'm':
        do_manual()
    elif fun == 'p':
        do_platooning()
    elif fun == 'd':
        do_drive(val)
    elif fun == 's':
        do_steer(val)


def do_manual():
    # print('I\'m manual!')
    pass


def do_acc(param):
    # print('I\'m ACC! ' + param)
    pass


def do_platooning():
    # print('I\'m platooning!')
    pass


def do_drive(param):
    # print("I'm driving!" + str(param))
    pass


def do_steer(param):
    # print("I'm steering!" + str(param))
    pass
