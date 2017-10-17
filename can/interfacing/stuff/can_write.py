import os
from _thread import start_new_thread


class CanWriter:
    def __init__(self):
        self.out_speed = 0
        self.out_steer = 0

    def can_send(self, speed, steer):
        cmd = "/home/pi/can-utils/cansend can0 '101#%02x%02x'" % (speed, steer)
        os.system(cmd)

    def start_cont_send(self):
        start_new_thread(continuous_send, (self,))  # Shorthand for sending via can-utils

    # if no value is given, it sends the last value to hold that value
    def send(self, input_speed=None, input_steer=None):

        if input_speed is None:
            input_speed = self.out_speed
        if input_steer is None:
            input_steer = self.out_steer

        self.out_speed = input_speed
        self.out_steer = input_steer


def continuous_send(writer):
    while 1:
        cmd = "/home/pi/can-utils/cansend can0 '101#%02x%02x'" % (writer.out_speed, writer.out_steer)
        os.system(cmd)