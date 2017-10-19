'''
    Simple socket server using threads
'''
import logging
import socket
import sys
# opens a socket and starts a thread listening for communication on that socket
import time
from _thread import start_new_thread

from state import State, char_to_state


class Communication():
    def __init__(self):
        self.data_log = None
        self.state = State.MANUAL
        self.steering = 0
        self.speed = 0
        self.acc_speed = 0

    def start_listen(self, port, host=''):
        self.data_log = []  # each thread writes to the same array (which might be a bad idea)

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

        start_new_thread(self.listen_thread, (s,))

        return self.data_log

        # thread listening for socket communication

    def listen_thread(self, s):
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
            try:
                data = raw_data.decode("utf-8").rstrip()
            except UnicodeDecodeError as e:
                logging.error("Closed %s@%s due to encoding error", address[0], str(address[1]))
                return
            self.data_log.append(data)

            self.interpret(data)

        # came out of loop
        conn.close()

    # decides what to do with a received message
    def interpret(self, data):
        if not data:
            return
        args = data.split(" ")

        function_charcode = args[0]
        self.state = char_to_state(function_charcode)

        val = None
        if len(args) > 1:
            val = args[1]

        self.do_function(function_charcode, val)

    # executes a function up to one value
    def do_function(self, fun, val):
        if fun == 'a':
            self.acc_speed = val
        elif fun == 'd':
            self.speed = val
            # self.do_drive(val)
        elif fun == 's':
            self.steering = val
            # self.do_steer(val)
