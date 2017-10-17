'''
    Simple socket server using threads
'''

import socket
import sys
from _thread import start_new_thread
import os

# opens a socket and starts a thread listening for communication on that socket


from driving import drive, steer


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
    connected_log = []
    while True:
        conn, address = s.accept()

        if address not in connected_log:
            connected_log.append(address)
            print("New client: " + address[0] + ':' + str(address[1]))

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

    val = None
    if len(args) > 1:
        val = args[1]

    do_function(fun, val)


# executes a function up to one value
def do_function(fun, val):
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
    drive(int(param))
    pass


def do_steer(param):
    # print("I'm steering!" + str(param))
    steer(int(param))
    pass
