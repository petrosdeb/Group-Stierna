'''unit testing for communication'''
import socket
import unittest
from time import sleep

import comm

PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("ip (maybe): " + s.getsockname()[0])
s.close()

data_log = comm.start_listen(PORT)
old_data = []

while True:
    if (data_log == old_data):
        continue
    old_data = data_log.copy()
    print(data_log)
