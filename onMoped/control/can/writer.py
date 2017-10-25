"""This module contains the CanWriter class
which acts as an easy way to continuously
write over the CAN"""
import logging
import os
import time
from _thread import start_new_thread


class CanWriter:
    """Usage:
    start_cont_send starts a thread which sends
    values on an interval. Sends the last
    values sent by send

    send is used to set the values to send """
    has_sent = True

    def __init__(self, can_device, can_path):
        self.out_speed = 0
        self.out_steer = 0
        self.can_device = can_device
        self.can_path = can_path

    def start_cont_send(self, frequency=10):
        """Starts a thread to send over the CAN
        on a set frequency"""
        logging.info("Starting continuous send")
        start_new_thread(self.__continuous_send, (frequency))

    # sets the value sent over can
    def send(self, input_speed=None, input_steer=None):
        """Sets the values to be sent over CAN
        No value means the last value is retained"""
        if input_speed is None:
            input_speed = self.out_speed
        if input_steer is None:
            input_steer = self.out_steer

        self.out_speed = int(input_speed)
        self.out_steer = int(input_steer)

    def __continuous_send(self, frequency):
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
            cmd = self.can_path + " " + self.can_device + " '101#%02x%02x'" \
                                                          % (send_speed, send_steer)
            os.system(cmd)
            self.has_sent = True

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("%d : continuous send active: (%d,%d)"
                             , c_time, send_speed, send_steer)
                last_time = c_time

            time.sleep(1 / frequency)
