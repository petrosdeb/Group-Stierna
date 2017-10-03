'''
    Simple socket server using threads
'''

import socket
import sys
import datetime
from thread import *

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'


# Function for handling connections. This will be used to create threads
def man():
    print "I'm manual!"


def acc():
    print "I'm ACC!"


def plt():
    print "I'm platooning!"


def doDrive(param):
    print "I'm driving"


def doSteer(param):
    print "I'm steering"


def clientthread(conn):
    data_log = []

    # Sending message to connected client
    conn.send('Connected to MOPED: ' + str(datetime.datetime.now()))  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = str(conn.recv(1024)).replace("\r\n", "")

        data_log.append(data)

        if not data:
            break

        # print 'r: ' + data + '\n'
        # Drive
        if data.startswith('d'):
            doDrive(int(data[1:]))
            print "Drive: " + data[1:]

        # Steer
        elif data.startswith('s'):
            doSteer(int(data[1:]))
            print "Steer: " + data[1:]


        # Manual
        elif data.startswith('m'):
            man()
            print "Switch to manual mode\n"

        # ACC
        elif data.startswith('a'):
            acc()
            print "Switch to acc mode\n"

        # Platooning
        elif data.startswith('p'):
            plt()
            print "Switch to platooning  mode\n"

    # came out of loop
    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))

s.close()
