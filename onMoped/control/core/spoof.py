"""
This module contains a class that simulates
the ultra control data in order to do off-
MOPED testing. Testing requires a a suitable
network device, e.g. a virtual CAN.

Notably, it does not write or receive over
CAN, but get_ultra_data control be used as if
it did. As a result, it enables testing all
    parts outside of can.control
"""
import math
import time
from _thread import start_new_thread

from core.interface import CoreInterface

DIST_VALUES = []

DATA = []

# Generate 10000 points of distance on the form of a sine wave
for i in range(1, 10000, 2):
    val = (math.sin(i / 40) + 1) * 30
    val = round(val, 2)
    DIST_VALUES.append(val)


class SpoofCore(CoreInterface):
    """Bare bones CoreInterface implementation
    with no other functionality that
    returning set values with
    get_ultra_data
    """

    def __init__(self):
        start_new_thread(self.__spoof_thread, ())

    def get_ultra_data(self, n=1):
        return DATA[-n:]

    # updates what values get_ultra_data returns
    @staticmethod
    def __spoof_thread():
        idx = 0
        while 1:
            time.sleep(0.2)
            DATA.append((time.clock(), DIST_VALUES[idx]))
            idx = (idx + 1) % 10000
