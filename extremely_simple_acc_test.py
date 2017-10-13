"""
An acc that in some ways tries to make use of a negative feedback loop, with a more effective brake
"""

import time
from driving import drive
from nav import *

#
def acc_test(ideal_distance):
    while True:
        keep_distance(ideal_distance)
        electric_brake(ideal_distance)

def keep_distance(ideal_distance):
    prev_distance = g.can_ultra
    sleep(0.1)
    distance = g.can_ultra
    while prev_distance < distance or distance > ideal_distance: #risk for stalling, most likely needs to be heavily adjusted
        sleep(0.05)
        drive(27) #just a random chosen value from "the list"
        prev_distance = distance
        distance = g.can_ultra
        


#set drive to -100 until ultra says distance to the car in front is not decreasing anymore
def electric_brake(ideal_distance):
    drive(0)
    prev_distance = g.can_ultra
    sleep(0.1)
    distance = g.can_ultra
    while prev_distance - distance > 5: #allow for error
        drive(-100)
        prev_distance = distance
        distance = g.can_ultra
    while distance < ideal_distance: #to avoid that the car crashes, that it does not stall and also waits for the other car to accelerate
        drive(0)


