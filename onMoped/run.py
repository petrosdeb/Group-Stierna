import logging
import sys

from core import Core

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

__default_port = 8888
__can_device = 'can0'
__can_utils_path = "/home/pi/can-utils/cansend"

if __name__ == '__main__' and len(sys.argv) > 1:

    skip = 0
    print(sys.argv)
    for idx, arg in enumerate(sys.argv):
        try:
            if skip:
                skip -= 1
                continue
            if arg == '--port' or arg == '-p':
                print("port {}".format(sys.argv[idx + 1]))
                __default_port = int(sys.argv[idx + 1])
                skip = 1
            if arg == '--can_device' or arg == '-d':
                __can_device = sys.argv[idx + 1]
                skip = 1
            if arg == '--can_utils_path' or arg == '-u':
                __can_utils_path = sys.argv[idx + 1]
                skip = 1
        except IndexError as e:
            logging.error("Missing arg for {}".format(arg))

core_inst = Core(port=__default_port, can_device=__can_device, can_utils_path=__can_utils_path)
