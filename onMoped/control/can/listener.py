"""This module contains the CanListener class
which is used to listen to communication over
a can-network"""

import logging
import re
import socket
import time
from _thread import start_new_thread


class CanListener:
    """Usage: calling socket_open opens a socket
    which passively listens for can-data and
    stores it as a (time, value) tuple.
    data_fetch to retrieve"""

    def __init__(self):
        self.dist_log = []
        self.sock = None

    def socket_close(self):
        """Closes the open socket"""
        logging.info("Closing socket")
        self.sock.shutdown()
        self.sock.close()

    def socket_open(self, network):
        """Opens a can-socket
        :param network a can-device such as can0"""
        logging.info("Opening %s socket . . .", network)
        self.sock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)

        try:
            self.sock.bind((network,))
        except socket.error as msg:
            print(msg)

        logging.info("Starting new socket listening thread...")
        start_new_thread(self.__listen_thread, ())

    def __dist_push_data__(self, value):
        self.dist_log.append(
            (time.clock(), value))

    def data_fetch(self, fetch_number=1):
        """Returns the latest data entries as a list of (time,value) tuples
        :param fetch_number the number to retrieve"""
        return self.dist_log[-fetch_number:]

    def __listen_thread(self, ):
        buffer = b""

        last_time = 0

        while True:

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("%d: %s is reading CAN \n data: %d",
                             c_time, type(self).__name__, self.data_fetch()[0])

                last_time = c_time

            data = self.sock.recv(64)
            if (data[0], data[1]) == (108, 4):  # control-bytes start like this (probably)
                if data[8] == 16:
                    if len(buffer) > 18:
                        buffer_filtered = buffer[19:]
                        buffer_filtered_decoded = buffer_filtered.decode('ascii')
                        msg_len = buffer[18]
                        buffer_msg_slice = buffer_filtered_decoded[0:msg_len]

                        # magic reg-ex stolen from legacy
                        msg = re.search("^([0-9]+) ([0-9]+) $", buffer_msg_slice)
                        if msg:
                            distance = int(msg.group(2))
                            # if d != 3400:
                            self.__dist_push_data__(distance)
                        buffer = b""
                        time.sleep(0.00001)
                buffer += data[9:]
