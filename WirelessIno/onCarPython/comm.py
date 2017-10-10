'''
    Simple socket server using threads
'''

import socket
import sys
import atexit
import datetime
from _thread import start_new_thread
import nav as n
from nav import *
from nav1 import whole4, pause, cont
from driving import stop, drive, steer
from constant_speed import constant_speed
from acc import activate_acc, on, acc, acc_on

import os

if len(sys.argv) > 1:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    print("Open socket " + HOST + " at port " + str(PORT))
else:
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 9000  # Arbitrary non-privileged port
    print("Open socket with default host at port" + str(PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')


# Function for handling connections. This will be used to create threads
def do_manual():
    print('I\'m manual!')


def do_acc():
    print('I\'m ACC!')


def do_platooning():
    print('I\'m platooning!')


def do_drive(param):
    drive(param)


def do_steer(param):
    steer(param)


# executes param[0] with param[1:] as the arguments
def run_python(param):
    cmd = ""
    for w in param:
        cmd = cmd + " " + w

    os.system(cmd)


# decides what to do with a received message
def interpret(data):
    if not data:
        return
    c = data[0]
    if c == 'a':
        do_acc()
    elif c == 'm':
        do_manual()
    elif c == 'p':
        do_platooning()
    elif c == 'd':
        do_drive(data[2:])
    elif c == 's':
        do_steer(data[2:])
    elif c == 'r':
        run_python(data[1:].split(" "))


# a new client_thread is opened whenever a new connection is established
def client_thread(conn):
    data_log = []

    # Sending message to connected client
    # conn.send('Connected to MOPED: ' + str(datetime.datetime.now()))  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.
    # while True:

    # Receiving from client
    data = str(conn.recv(1024))

    data = data[2:len(data) - 3]

    print(data)

    data_log.append(data)

    # if not data:
    #   break

    interpret(data)
    # came out of loop
    conn.close()  # now keep talking with the client


while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(client_thread, (conn,))


# @atexit
# def exit():
# if not s:
#     return
#  s.close()
