import re
import socket
import sys
import time
from _thread import start_new_thread


class CanListener:
    def __init__(self):
        self.dist_log = []
        self.sock = None

    def socket_close(self):
        self.sock.shutdown()
        self.sock.close()

    # opens a socket (using the can0-interface by default)
    def socket_open(self, network='can0'):
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
            (time.time(), value))
        print(self.dist_log[-1])

    def data_fetch(self):
        pass  # TODO return some form of data

    def listen_thread(self, varargs=None):
        part2 = b""

        while True:
            data = self.sock.recv(64)
            if (data[0], data[1]) == (108, 4):  # can-bytes start like this (probably)
                if data[8] == 16:
                    if len(part2) > 18:
                        part2x = part2[19:]
                        part2s = part2x.decode('ascii')
                        l = part2[18]
                        part2s2 = part2s[0:l]

                        m = re.search("^([0-9]+) ([0-9]+) $", part2s2)
                        if m:
                            d = int(m.group(2))
                            self.__dist_push_data__(d)
                        part2 = b""
                        time.sleep(0.00001)
                part2 += data[9:]


def data_is_ultra(data):
    return (data[0], data[1]) == (108, 4) and data[8] == 16
