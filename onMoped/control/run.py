"""Init script for the control-package."""

import logging
import sys

from core.concrete import CoreConcrete

DEFAULT_PORT = 8888
CAN_DEVICE = 'can0'
CAN_UTILS_PATH = "/home/pi/control-utils/cansend"
SPOOF_DATA = False

# DIY argparser
# (TODO implement proper argparse)
if __name__ == '__main__' and len(sys.argv) > 1:
    SKIP = 1
    ARGS = sys.argv
    for idx, arg in enumerate(ARGS):
        try:
            if SKIP:
                SKIP -= 1
                continue

            if arg == '--port' or arg == '-p':
                DEFAULT_PORT = int(ARGS[idx + 1])
                SKIP = 1

            if arg == '--can_device' or arg == '-d':
                CAN_DEVICE = ARGS[idx + 1]
                SKIP = 1

            if arg == '--can_utils_path' or arg == '-u':
                CAN_UTILS_PATH = ARGS[idx + 1]
                SKIP = 1

            if arg == '--error_level' or arg == '-e':
                logging.basicConfig(stream=sys.stderr, level=int(ARGS[idx + 1]))
                SKIP = 1

            if arg == '--spoof_data' or arg == '-s':
                SPOOF_DATA = True

        except IndexError:
            print("Missing arg for {}".format(arg))

# Set the default logger level (if written beforehand, this is ignored)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

logging.info("Init core, port %d, device %s, utils_path %s",
             DEFAULT_PORT, CAN_DEVICE, CAN_UTILS_PATH)

# Instantiate the main process
CORE_INST = CoreConcrete(
    port=DEFAULT_PORT,
    can_device=CAN_DEVICE,
    can_utils_path=CAN_UTILS_PATH,
    spoof_core=SPOOF_DATA)
