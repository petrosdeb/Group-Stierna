import logging
import sys

from core import Core

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

port = 8888
can_device = 'can0'
can_utils_path = "/home/pi/can-utils/cansend"

if __name__ == '__main__' and len(sys.argv) > 1:

    skip = 1
    for idx, arg in enumerate(sys.argv):
        try:
            if skip:
                continue
            if arg == '--port' or arg == '-p':
                port = arg[idx + 1]
            if arg == '--can_device' or arg == '-d':
                port = arg[idx + 1]
            if arg == '--can_utils_path' or arg == '-u':
                port = arg[idx + 1]
        except IndexError as e:
            logging.error("Missing arg for {}".format(arg))

core = Core()
