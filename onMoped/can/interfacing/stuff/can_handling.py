from time import sleep

from stuff.can_listen import CanListener

listener = CanListener()

while 1:
    data = listener.data_fetch(10)
    
    
    sleep(0.05)