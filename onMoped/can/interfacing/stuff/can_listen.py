import re
import socket
import sys
import time
from _thread import start_new_thread

from can.interfacing.stuff import can_write


class CanListener:
    def __init__(self):
        self.dist_log = []
        self.sock = None

    def socket_close(self):
        print("Closing socket")
        self.sock.shutdown()
        self.sock.close()

    # opens a socket (using the can0-interface by default)
    def socket_open(self, network=can_write.CAN_DEVICE):
        print("Opening " + network + " socket...")
        self.sock = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)

        try:
            self.sock.bind((network,))
        except socket.error as msg:
            print(msg)
            sys.exit(1)

        print("Starting new socket listening thread...")
        start_new_thread(self.listen_thread, (self,))

    def __dist_push_data__(self, value):
        self.dist_log.append(
            (time.clock(), value))

    def data_fetch(self, fetchNumber):
        return self.dist_log[-fetchNumber:]

    def listen_thread(self, varargs=None):
        buffer = b""

        last_time = 0

        while True:

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                print(str(c_time) + ': ' + type(self).__name__ + ' is reading CAN')  # usch
                print(self.data_fetch(10))
                last_time = c_time

            data = self.sock.recv(64)
            if (data[0], data[1]) == (108, 4):  # can-bytes start like this (probably)
                if data[8] == 16:
                    if len(buffer) > 18:
                        buffer_filtered = buffer[19:]
                        buffer_filtered_decoded = buffer_filtered.decode('ascii')
                        msg_len = buffer[18]
                        buffer_msg_slice = buffer_filtered_decoded[0:msg_len]

                        m = re.search("^([0-9]+) ([0-9]+) $", buffer_msg_slice)  # idk what this actually does
                        if m:
                            d = int(m.group(2))
                            self.__dist_push_data__(d)
                        buffer = b""
                        time.sleep(0.00001)
                buffer += data[9:]
