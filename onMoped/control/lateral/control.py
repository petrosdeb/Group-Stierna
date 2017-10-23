"""
    This file contains functions to calculate steering direction
    for a "moped" (see github.com/sics-sse/moped)
"""
import logging
import time

import driving as CRL_CAR
import picamera

from control.lateral import navigation

# Parameters used to set picamera image resolution
# Size: pixels in X-axis

RESOLUTIONX = 1024
# Size: pixels in Y-axis
RESOLUTIONY = 764


def main():
    """
        Captures image, tries to find a barcod once found it is sent to
        adapt_steering which sets the steering. This will loop
    """
    camera = picamera.PiCamera()
    camera.resolution = (RESOLUTIONX, RESOLUTIONY)
    camera.iso = 800
    time.sleep(2)
    while True:
        camera.capture('current-image.jpg')
        adapt_steering(navigation.get_xposition('current-image.jpg'))
        time.sleep(0.4)


def adapt_steering(position):
    """
        Calculates a steer-signal, sets steerdirection
        and prints the calculated value
    """
    center = RESOLUTIONX / 2
    offset = center - position
    steerfactor = offset / 10
    CRL_CAR.steer(steerfactor)
    logging.info(position)
