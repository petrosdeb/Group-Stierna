"""This module contains an interface for the
core of the program, responsible for writing
and reading data between different processes
"""


class CoreInterface:
    def get_ultra_data(self, n=1):
        """Returns the last n ultra data entries
    from the CAN"""
        pass
