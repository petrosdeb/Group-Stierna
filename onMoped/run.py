import logging
import sys

from core import Core

# myv: vcan0, cansend

# Checks the command line arguments, should be replaced with a parser


__default_port = 8888
__can_device = 'can0'
__can_utils_path = "/home/pi/can-utils/cansend"

if __name__ == '__main__' and len(sys.argv) > 1:
    skip = 0
    args = sys.argv
    for idx, arg in enumerate(args):
        try:
            if skip:
                skip -= 1
                continue

            if arg == '--port' or arg == '-p':
                __default_port = int(args[idx + 1])
                skip = 1

            if arg == '--can_device' or arg == '-d':
                __can_device = args[idx + 1]
                skip = 1

            if arg == '--can_utils_path' or arg == '-u':
                __can_utils_path = args[idx + 1]
                skip = 1

            if arg == '--error_level' or arg == '-e':
                logging.basicConfig(stream=sys.stderr, level=int(args[idx + 1]))
                skip = 1

        except IndexError as e:
            print("Missing arg for {}".format(arg))

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

logging.info("Init core, port {}, device {}, utils_path {}".format(__default_port, __can_device, __can_utils_path))

core_inst = Core(port=__default_port, can_device=__can_device, can_utils_path=__can_utils_path)
