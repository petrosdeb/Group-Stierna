import logging
from _thread import start_new_thread
from enum import Enum

import time

import sys

from acc import Acc
from can.interfacing.stuff.can_listen import CanListener
from can.interfacing.stuff.can_write import CanWriter
from comm import Communication
from state import State


class Core():
    def __init__(self,
                 port=8888,
                 can_device='can0',
                 can_utils_path=' /home/pi/can-utils/cansend'):

        self.speed = 0
        self.steering = 0
        self.state = State.MANUAL

        logging.info("Starting CanListener")
        self.listener = CanListener()
        self.listener.socket_open(can_device)

        logging.info("Starting ACC")
        self.acc = Acc(self)

        logging.info("Starting CanWriter")
        self.writer = CanWriter(can_device=can_device, can_path=can_utils_path)
        self.writer.start_cont_send()

        logging.info("Starting Communication")
        self.communicator = Communication()
        self.communicator.start_listen(port)

        logging.info("Starting core thread")
        start_new_thread(self.__core_thread, ())

    def get_ultra_data(self, n=1):
        return self.listener.data_fetch(n)

    def __core_thread(self):

        last_time = 0
        while True:

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("{} : {} is running, state= {}".format(c_time, type(self).__name__, self.state))
                last_time = c_time

            temp_state = self.communicator.state
            if temp_state != None:
                self.state = temp_state

            self.acc.wanted_speed = self.communicator.acc_speed

            if self.state == State.MANUAL:
                self.speed = self.communicator.speed
                self.steering = self.communicator.steering
            if self.state == State.ACC:
                self.speed = self.acc.speed
                self.steering = self.communicator.steering
            elif self.state == State.PLATOONING:
                self.speed = 0
                self.steering = 0

            self.acc.current_speed = self.speed
            self.writer.send(self.speed, self.steering)
