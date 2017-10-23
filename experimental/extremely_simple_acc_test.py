"""
Effort to try to construct a working ACC by simplifying it.
"""

import time
from driving import drive
from nav import *


def acc_test(ideal_distance, use_electric):
    '''
    Main method to run ACC
    '''
    while True:
        keep_distance(ideal_distance)
        if use_electric:
            electric_brake(ideal_distance)
        else:
            brake(ideal_distance)

def keep_distance(ideal_distance):
    '''
    Adjusts speed to keep distance
    '''
    prev_distance = g.can_ultra
    time.sleep(0.1)
    distance = g.can_ultra
    #risk for stalling, most likely needs to be heavily adjusted
    while prev_distance < distance or distance > ideal_distance:
        drive(19) #just a random chosen value from "the list"
        prev_distance = distance
        time.sleep(0.05)
        distance = g.can_ultra


#set drive to -100 until ultra says distance to the car in front is not decreasing anymore
def electric_brake(ideal_distance):
    '''
    If the MOPED approaches the preceding MOPED by more than 1 cm per every tenth of a second,
    the car brakes.
    Also the distance to the preceding car has to be less than the ideal distance.
    Otherwise there is no reason to brake.
    '''
    drive(0)
    prev_distance = g.can_ultra
    time.sleep(0.1)
    distance = g.can_ultra
    while prev_distance - distance > 0.01 and distance < ideal_distance:
        drive(-100)
        prev_distance = distance
        drive(0)
        time.sleep(0.1)
        distance = g.can_ultra
    #If distance isn't decreasing, we wait until the preceding car is accelerating
    #and to avoid that the car crashes
    while distance < ideal_distance:
        drive(0)

def brake(ideal_distance):
    '''
    Normal brake should be enough.
    Simply setting the speed to 0 gives a braking distance of 1 cm/(cm/s).
    So it should definitely be good enough if we set the ideal distance high enough.
    '''
    distance = g.can_ultra
    prev_distance = distance
    while prev_distance - distance > 0.01 or distance < ideal_distance:
        prev_distance = distance
        drive(0)
        time.sleep(0.1)
        distance = g.can_ultra
