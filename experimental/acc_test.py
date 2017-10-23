'''
Basic working ACC, with safety in mind.
Made to avoid crashing into MOPEDs and other objects.
'''

from driving import drive

# adjust speed according to distance to preceding vehicle, to match its speed
def activate_acc(set_d):
    '''
    Simple ACC that aims that takes desired distance as parameter
    '''
    while True:
        distance = g.can_ultra
        speed = 0
        while distance > set_d:
            speed += 1
            drive(speed)
        while distance < set_d:
            speed -= 1
            drive(speed)

def act_acc(set_d, brake, desired_speed):
    '''
    Working implementation
    Our main ACC function
    set_d: minimum distance to the preceding MOPED desired, in meters
    brake: takes input 0, 1, 2 for different brake methods used.
    Defaults to 0 if faulty input is given
    '''
    if brake != (0 or 1 or 2):
        brake = 0
    print(brake)
    #set true if the car has stopped
    stopped = True
    while True:
        distance = g.can_ultra
        print(distance)

        #as long as distance is less than desired distance, keep speed
        while distance > set_d:
            speed = desired_speed
            drive(speed)
            distance = g.can_ultra

            #With the new distance, yet again check if the distance is larger than desired distance.
            #Set stopped to False as the car is ready to drive
            if distance > set_d:
                stopped = False
            print(distance)

        #if distance is smaller than desired distance, brake.
        #we have several different brake functions,
        #depending on whether aggressive braking is needed or not
        #for aggressive braking electric brake is used, for less aggressive
        #brake use decremental brake.
        #distance based brake aims to keep the set_d to the car in front
        #Electric brake runs the risk of stalling and reversing.
        #Therefore using it only allows for braking
        #when distance is larger than 10 cm.
        while 0 < distance < set_d:
            distance = g.can_ultra

            if brake == 0:
                if not stopped:
                    electric_braking()
                    print(distance)
                    if distance < 0.05:
                        stopped = True
                        drive(0)
            elif brake == 1:
                distance_based_brake(set_d)
            elif brake == 2:
                decremental_brake(speed)
            else:
                drive(0)

                print(distance)

def electric_braking():
    '''
    The most effective brake.
    Should only be used for safety or in case of very high speeds.
    '''
    amount = 10
    while amount > 0:
        drive(-100)
        amount -= 1


def decremental_brake(speed):
    '''
    Brakes in small increments to avoid stalling
    '''
    for number in range(0, speed):
        drive(speed - (number + 1))

def distance_based_brake(set_d):
    '''
    Brakes in small increments to avoid stalling,
    but at the same time to be very effective
    '''
    distance = g.can_ultra
    if distance < set_d:
        speed = g.outspeedcm/2
        while speed > 0:
            speed -= 5
            if speed < 0:
                speed = 0
            drive(speed)


def acc_speed(speed, set_d):
    '''
    Small incremental ACC that works for very small speeds or
    with frequent data
    '''
    distance = g.can_ultra
    current_speed = g.outspeedcm/2
    while True:
        while distance > set_d and current_speed < speed:
            increase_speed(current_speed)
            current_speed = g.outspeedcm/2
            distance = g.can_ultra
        while distance < set_d:
            electric_braking()
            drive(0)
            distance = g.can_ultra
            current_speed = g.outspeedcm/2
        while distance > set_d and current_speed > speed:
            decrease_speed(current_speed)
            current_speed = g.outspeedcm/2
            distance = g.can_ultra

def increase_speed(current_speed):
    '''
    Increases speed with a unit of one
    '''
    speed = current_speed + 1
    drive(speed)

def decrease_speed(current_speed):
    '''
    Decreases speed with a unit of one
    '''
    speed = current_speed - 1
    drive(speed)
    