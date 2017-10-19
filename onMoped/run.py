from core import Core
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

__default_port = 8888
__can_device = 'can0'
__can_utils_path = "/home/pi/can-utils/cansend"

if __name__ == '__main__' and len(sys.argv) > 1:

    skip = 1
    for idx, arg in enumerate(sys.argv):
        try:
            if skip:
                continue
            if arg == '--port' or arg == '-p':
                default_port = arg[idx + 1]
            if arg == '--can_device' or arg == '-d':
                default_port = arg[idx + 1]
            if arg == '--can_utils_path' or arg == '-u':
                default_port = arg[idx + 1]
        except IndexError as e:
            logging.error("Missing arg for {}".format(arg))

core_inst = Core(port=__default_port, can_device=__can_device, can_utils_path=__can_utils_path)
