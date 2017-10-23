import logging
import socket
import sys
import time
from _thread import start_new_thread

from control.state import State, char_to_state

'''
Class for handling outside communication,
implementing a simple server-style socket


On the MOPED, this is used to receive inputs 
from an  Android-application
'''


class CommunicationHandler():
    def __init__(self):
        self.state = State.MANUAL
        self.steering = 0
        self.speed = 0
        self.acc_speed = 0

    # initiates the socket and starts the listen thread
    def start_listen(self, port, host=''):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logging.info('Socket created: \'' + host + '\'@' + str(port))

        try:
            s.bind((host, port))
        except socket.error as msg:
            logging.error(msg)
            sys.exit(1)

        logging.info('Socket bind complete')
        s.listen(10)

        logging.info('Socket now listening')

        start_new_thread(self.__listen_thread, (s,))

    # thread waiting for connecting sockets
    def __listen_thread(self, s):
        logging.info('Listening thread started')
        connected_log = []
        last_time = time.time()

        while True:
            conn, address = s.accept()

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("{}: {} is listening to connections".format(c_time, type(self).__name__))
                last_time = c_time

            if address[0] not in connected_log:
                connected_log.append(address[0])
                logging.info("New client: {}@{}".format(address[0], address[1]))

            start_new_thread(self.__client_thread, (conn, address))

    # a new client_thread is opened whenever a new connection is established
    def __client_thread(self, conn, address):
        # infinite loop so that function do not terminate and thread do not end.
        while True:
            # Receiving from client
            raw_data = conn.recv(1024)

            if not raw_data:
                break

            # Skip the surrounding junk
            try:
                data = raw_data.decode("utf-8").rstrip()
            except UnicodeDecodeError as e:
                logging.error("Closed %s@%s due to encoding error", address[0], str(address[1]))
                return

            self.__interpret(data)

        # came out of loop
        conn.close()

    # decides what to do with a received message
    def __interpret(self, data):
        if not data:
            return
        args = data.split(" ")

        function_charcode = args[0]
        self.state = char_to_state(function_charcode)

        val = None
        if len(args) > 1:
            val = args[1]

        self.__do_command(function_charcode, val)

    # executes a function up to one value
    def __do_command(self, fun, val):
        if fun == 'a':
            self.acc_speed = val
        elif fun == 'd':
            self.speed = val
            # self.do_drive(val)
        elif fun == 's':
            self.steering = val
            # self.do_steer(val)
