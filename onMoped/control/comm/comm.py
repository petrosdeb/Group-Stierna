"""This module contains the CommunicationHandler
that reads data from a socket, for use with
an Android app"""
import logging
import socket
import sys
import time
from _thread import start_new_thread

from state import State, char_to_state


class CommunicationHandler:
    """The class is self-serving and can be
    polled for values on-demand, i.e.
        state
        steering
        speed
        acc_speed

    Usage:
    start_listen needs to be called to start
    the listening thread"""

    def __init__(self):
        self.state = State.MANUAL
        self.steering = 0
        self.speed = 0
        self.acc_speed = 0

    # initiates the socket and starts the listen thread
    def start_listen(self, port, host=''):
        """Starts listening for connecting sockets"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logging.info('Socket created: \'' + host + '\'@' + str(port))

        try:
            sock.bind((host, port))
        except socket.error as msg:
            logging.error(msg)
            sys.exit(1)

        logging.info('Socket bind complete')
        sock.listen(10)

        logging.info('Socket now listening')

        start_new_thread(self.__listen_thread, (sock,))

    # thread waiting for connecting sockets
    def __listen_thread(self, sock):
        logging.info('Listening thread started')
        connected_log = []
        last_time = time.time()

        while True:
            conn, address = sock.accept()

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("%d: %s is listening to connections",
                             c_time, type(self).__name__)
                last_time = c_time

            if address[0] not in connected_log:
                connected_log.append(address[0])
                logging.info("New client: %s@%d", address[0], address[1])

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
            except UnicodeDecodeError:
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
