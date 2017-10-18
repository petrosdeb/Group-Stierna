import logging
import sys

from core import Core

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

if __name__ == '__main__' and len(sys.argv) > 1:
    core = Core(int(sys.argv[1]))
else:
    core = Core()
