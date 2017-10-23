from enum import Enum

'''
Simple enum-class representing the 3 driving 
states of the MOPED.

Used in core to determine what output values
are written
'''


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
