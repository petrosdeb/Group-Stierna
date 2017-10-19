import logging
import os
from _thread import start_new_thread

import time
import math


class CanWriter:
    def __init__(self, can_device, can_path):
        self.out_speed = 0
        self.out_steer = 0
        self.can_device = can_device
        self.can_path = can_path

    def can_send(self, speed, steer):
        cmd = self.can_path + " " + self.can_device + " '101#%02x%02x'" % (speed, steer)
        os.system(cmd)

    def start_cont_send(self):
        logging.info("Starting continuous send")
        start_new_thread(self.continuous_send, ())  # Shorthand for sending via can-utils

    # if no value is given, it sends the last value to hold that value
    def send(self, input_speed=None, input_steer=None):

        if input_speed is None:
            input_speed = self.out_speed
        if input_steer is None:
            input_steer = self.out_steer

        self.out_speed = int(input_speed)
        self.out_steer = int(input_steer)

    def continuous_send(self):
        last_time = time.time()

        while 1:

            send_steer = max(self.out_steer, -60)
            send_speed = self.out_speed

            # wrap around steer values
            if send_steer < 0:
                send_steer = 201 + send_steer

            if send_speed < 0:
                send_speed = 201 + send_speed

            # 101#A00F
            cmd = self.can_path + " " + self.can_device + " '101#%02x%02x'" % (send_speed, send_steer)
            os.system(cmd)

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("{} : continuous send active: {}".format(c_time, (send_speed, send_steer)))  # usch
                last_time = c_time

            time.sleep(0.01)
