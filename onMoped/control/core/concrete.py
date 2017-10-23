import logging
import time
from _thread import start_new_thread

from control.acc.handler import AccHandler
from control.comm.comm import CommunicationHandler
from control.core.interface import CoreInterface
from control.core.spoof import SpoofCore
from control.state import State

'''
A real implementation of CoreInterface

Initiates sub-processes, usually running in
a separate thread, and reads/supplies the data 
between them.
'''


class CoreConcrete(CoreInterface):
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
        c = self
        if spoof_core:
            c = SpoofCore()
        self.acc = AccHandler(c)

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
            if not self.writer.hasSent:
                continue

            self.writer.hasSent = True

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                logging.info("{} : {} is running, state= {}".format(c_time, type(self).__name__, self.state))
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
