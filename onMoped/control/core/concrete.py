"""This module includes the concrete
implementation of CoreInterface"""

import logging
import time
from _thread import start_new_thread

from acc.handler import AccHandler
from can.listener import CanListener
from can.writer import CanWriter
from comm.comm import CommunicationHandler
from core.interface import CoreInterface
from core.spoof import SpoofCore
from state import State


class CoreConcrete(CoreInterface):
    """
    A real implementation of CoreInterface

    Initiates sub-processes, usually running in
    a separate thread, and reads/supplies the data
    between them.
    """

    def __init__(self,
                 port,
                 can_device,
                 can_utils_path,
                 spoof_core=False):

        self.speed = 0
        self.steering = 0
        self.state = State.MANUAL

        logging.info("Starting CanListener")
        self.listener = CanListener()
        self.listener.socket_open(can_device)

        logging.info("Starting ACC")
        acc_core = self
        if spoof_core:
            acc_core = SpoofCore()
        self.acc = AccHandler(acc_core)

        logging.info("Starting CanWriter")
        self.writer = CanWriter(can_device=can_device, can_path=can_utils_path)
        self.writer.start_cont_send()

        logging.info("Starting Communication")
        self.communicator = CommunicationHandler()
        self.communicator.start_listen(port)

        logging.info("Starting core thread")
        start_new_thread(self.__core_thread, ())

    # returns the last n ultra data values
    def get_ultra_data(self, n=1):
        return self.listener.data_fetch(n)

    def __core_thread(self):

        last_time = 0
        while True:
            if not self.writer.has_sent:
                continue

            self.writer.has_sent = True

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("%d : %s is running, state= %s",
                             c_time, type(self).__name__, self.state)
                last_time = c_time

            temp_state = self.communicator.state
            if temp_state != None:
                self.state = temp_state

            self.acc.wanted_speed = int(self.communicator.acc_speed)

            if self.state == State.MANUAL:
                self.speed = self.communicator.speed
                self.steering = self.communicator.steering
            if self.state == State.ACC:
                self.speed = self.acc.speed
                self.steering = self.communicator.steering
            elif self.state == State.PLATOONING:
                self.speed = 0
                self.steering = 0

            self.acc.current_speed = int(self.speed)
            self.writer.send(self.speed, self.steering)
