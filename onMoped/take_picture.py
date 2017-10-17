from time import sleep
import picamera
from driving import steer
from nav import *



def tcapture():
    camera = picamera.PiCamera()
    camera.resolution = (1024,768)
    camera.capture("picture.jpg")

def test_steer():
    while(True):
        sleep(2)
        x = take_picture()
        steer(x/10)



test_steer()







