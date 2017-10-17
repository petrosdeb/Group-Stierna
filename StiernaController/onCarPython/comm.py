'''
    Simple socket server using threads
'''

import socket
import sys
from _thread import start_new_thread
import os

# opens a socket and starts a thread listening for communication on that socket


from driving import drive, steer


class Communication():
    def __init__(self):
        self.data_log = None
        self.state = 'm'
        self.steering = 0
        self.speed = 0

    def start_listen(self, port, host=''):
        self.data_log = []  # each thread writes to the same array (which might be a bad idea)

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

        start_new_thread(self.listen_thread, (s,))

        return self.data_log

    # thread listening for socket communication
    def listen_thread(self, s):
        connected_log = []
        while True:
            conn, address = s.accept()

            if address not in connected_log:
                connected_log.append(address)
                print("New client: " + address[0] + ':' + str(address[1]))

            start_new_thread(self.client_thread, (conn, address))

    # a new client_thread is opened whenever a new connection is established
    def client_thread(self, conn, address):
        # infinite loop so that function do not terminate and thread do not end.
        while True:

            # Receiving from client
            raw_data = conn.recv(1024)

            if not raw_data:
                break

            # Skip the surrounding junk
            data = raw_data.decode("utf-8").rstrip()

            self.data_log.append(data)
            # print(data_log)

            self.interpret(data)

        # came out of loop
        conn.close()  # now keep talking with the client
        #  print('Connection closed: ' + address[0] + ':' + str(address[1]))

    # decides what to do with a received message
    def interpret(self, data):
        if not data:
            return
        args = data.split(" ")

        fun = args[0]
        self.state = fun

        val = None
        if len(args) > 1:
            val = args[1]

        self.do_function(fun, val)

    # executes a function up to one value
    def do_function(self, fun, val):
        if fun == 'd':
            self.speed = val
            # self.do_drive(val)
        elif fun == 's':
            self.steering = val
            # self.do_steer(val)

    def do_manual(self):
        # print('I\'m manual!')
        pass

    def do_acc(self, param):
        # print('I\'m ACC! ' + param)
        pass

    def do_platooning(self):
        # print('I\'m platooning!')
        pass

    def do_drive(self, param):
        # print("I'm driving!" + str(param))
        drive(int(param))
        pass

    def do_steer(self, param):
        # print("I'm steering!" + str(param))
        steer(int(param))
        pass
