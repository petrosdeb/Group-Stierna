'''
acc using relative speed

issue 1. Do we need to set g.braking = True when we are braking?

The reaction time is 0,25 seconds. Meaning the distance to the preceding car has to be at least speed/4.
If the car is driving 3 m/s, then the distance has to be at least ,75 meters. However the sensor can
detect distances of up to 3,7 meters, so initially we should set distance to be greater than ,75 meters.
'''

import time
from driving import drive
from nav import *



#use_electric = True to use electric brake
def acc_run_test(use_electric):
    while True:
        
        prev_distance = g.can_ultra
        sleep(0.25) #Supposedly only gets a value four times per second
        distance = g.can_ultra
        relative_speed = calc_relative_speed(prev_distance, distance, 0.25)
        
        if relative_speed >= 0 and distance > 1: #increase speed, but for now only set to 19
            drive(19)
        else:
            if use_electric:
                electric_braking()
            else:
                drive(0)

#modify and calibrate
def electric_braking():
    for x in range(0, 10):
        drive(-100)
    drive(0)


'''
Positive value if distance to preceding car is decreasing, else negative.
'''
def calc_relative_speed(prev, current, time):
    distance_change = prev - current
    return distance_change/time
