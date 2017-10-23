'''
acc using relative speed

The reaction time is 0,25 seconds.
Meaning the distance to the preceding car has to be at least speed/4.
The sensor can detect distances of up to 3,7 meters.
Initially we set ideal distance to be greater than ,75 meters.
'''

import time
from driving import drive
from nav import *

def average_distance(amount):
    '''
    Calculates average distance to preceding car.
    time = amount/10
    '''
    total_distance = 0
    times = 0
    while times < amount:
        time.sleep(0.1)
        total_distance = total_distance + g.can_ultra
        times += 1
    return total_distance/amount

#use_electric = True to use electric brake
def acc_run_test(use_electric):
    '''
    Handles braking and logic for ACC
    '''
    while True:
        prev_distance = g.can_ultra
        time.sleep(0.25) #Supposedly only gets a value four times per second
        distance = g.can_ultra
        relative_speed = calc_relative_speed(prev_distance, distance, 0.25)
        print(relative_speed)
        #check is distance has changed over several or one seconds
        #Calculate relative speed over a longer interval
        if relative_speed >= 0 or distance > 1: #increase speed, but for now only set to 19
            drive(19)
        else:
            if use_electric:
                electric_braking()
            else:
                drive(0)

def electric_braking():
    '''
    Electric brake
    '''
    times = 0
    while times < 10:
        drive(-100)
        times += 1
    drive(0)


def calc_relative_speed(prev, current, delta_time):
    '''
    Positive value if distance to preceding car is decreasing, else negative.
    '''
    distance_change = prev - current
    return distance_change/delta_time
