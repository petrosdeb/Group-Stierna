from _thread import start_new_thread
from enum import Enum

from StiernaController.onCarPython.comm import Communication
from onMoped.acc import Acc
from onMoped.can.interfacing.stuff.can_listen import CanListener
from onMoped.can.interfacing.stuff.can_write import CanWriter


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
    def __init__(self):
        self.listener = CanListener()
        self.listener.socket_open()

        self.acc = Acc(self)

        self.writer = CanWriter()
        self.writer.start_cont_send()

        self.state = State.ACC

        self.communicator = Communication()
        self.communicator.start_listen(8888)

        self.speed = 0
        self.steering = 0

        start_new_thread(self.active_thread, ())

    def get_ultra_data(self, n=1):
        return self.listener.data_fetch(n)

    def active_thread(self):
        while True:
            self.state = State.char_to_state(self.communicator.state)

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