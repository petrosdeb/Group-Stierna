import sys

from core import Core

if __name__ == '__main__':
    core = Core(int(sys.argv[1]))
else:
    core = Core()

print("Creating core")
