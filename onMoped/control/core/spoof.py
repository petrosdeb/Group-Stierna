import math
import time
from _thread import start_new_thread

from core.interface import CoreInterface

dist_values = []

data = []

'''
Module that simulates the ultra control data in order to do
off-MOPED testing. Testing requires a a suitable network-
device, e.g. a virtual CAN.

Notably, it does not write or recieve over CAN, but
get_ultra_data control be used as if it did. As a result, 
it enables testing all parts outside of can.control
'''
# Generate 10000 points of distance on the form of a sine wave
for i in range(1, 10000, 2):
    val = (math.sin(i / 40) + 1) * 30
    val = round(val, 2)
    dist_values.append(val)


class SpoofCore(CoreInterface):
    def __init__(self):
        start_new_thread(self.spoof_thread, ())

    def get_ultra_data(self, n=1):
        return data[-n:]

    # updates what values get_ultra_data returns
    @staticmethod
    def spoof_thread():
        idx = 0
        while 1:
            time.sleep(0.2)
            data.append((time.clock(), dist_values[idx]))
            idx = (idx + 1) % 10000
