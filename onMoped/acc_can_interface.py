from acc import *

from onMoped.can.interfacing.stuff.can_listen import CanListener


class AccCanInterface(): # TODO Replace with better class
    def __init__(self):
        self.listener = CanListener
        self.listener.socket_open(listener)

    def get_listener(self):
        return self.listener

    def remove_listener(self):
        self.listener.socket_close()
        self.listener = None
