'''
acc using relative speed
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
        
        if relative_speed >= 0: #increase speed, but for now only set to 19
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
