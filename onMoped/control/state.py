"""
Simple enum-class representing the 3 driving
states of the MOPED.

Used in core to determine what output values
are written
"""
from enum import Enum


class State(Enum):
    """Basic enum class"""
    UNDEF = -1
    MANUAL = 0
    ACC = 1
    PLATOONING = 2


def char_to_state(char):
    """Returns a State for a given character"""
    if char == 'm':
        return State.MANUAL
    elif char == 'a':
        return State.ACC
    elif char == 'p':
        return State.PLATOONING
    return State.UNDEF
