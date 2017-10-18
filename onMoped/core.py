from _thread import start_new_thread
from enum import Enum

import time
from acc import Acc
from can.interfacing.stuff.can_listen import CanListener
from can.interfacing.stuff.can_write import CanWriter
from comm import Communication


class State(Enum):
    MANUAL = 0
    ACC = 1
    PLATOONING = 2


def char_to_state(char):
    if char == 'm':
        return State.MANUAL
    elif char == 'a':
        return State.ACC
    elif char == 'p':
        return State.PLATOONING


class Core():
    def __init__(self, port=8888):
        self.speed = 0
        self.steering = 0
        self.state = State.MANUAL

        print("Starting CanListener")
        self.listener = CanListener()
        self.listener.socket_open()

        print("Starting acc")
        self.acc = Acc(self)

        print("Starting CanWriter")
        self.writer = CanWriter()
        self.writer.start_cont_send()

        print("Starting Communication")
        self.communicator = Communication()
        self.communicator.start_listen(port)

        print("Starting core thread")
        start_new_thread(self.__core_thread, ())

    def get_ultra_data(self, n=1):
        return self.listener.data_fetch(n)

    def __core_thread(self):

        last_time = 0
        while True:

            c_time = int(time.time())
            if c_time % 5 == 0 and c_time != last_time:
                print(str(c_time) + ': ' + type(self).__name__ + ' is running. . .state = ' + str(self.state))  # usch
                last_time = c_time

            self.state = char_to_state(self.communicator.state)
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

            self.writer.send(self.speed, self.steering)
