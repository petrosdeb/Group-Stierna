import logging
import time

from _thread import start_new_thread
from math import ceil, floor
#from acc_test import act_acc


class Acc():
    DISTANCE_CAP_METRES = 3
    DISTANCE_CAP_CENTIMETRES = DISTANCE_CAP_METRES * 100
    SAFE_DISTANCE = 40
    WANTED_DISTANCE = 50
    DIST_DATA_LIFETIME = 1

    def __init__(self, core):
        self.distance_list = []
        self.distance_time_list = []
        self.core = core
        self.drive(0)
        self.wanted_speed = 0
        self.current_speed = 0

        self.debug_string = ""

        start_new_thread(self.__acc_on, ())

        

    def __acc_on(self): #set_d, brake
        
        logging.info("Started acc_on")

        last_time = time.time()
        set_d = 1
        brake = 0
        
        if brake != 0 or brake != 1 or brake != 2:
                brake = 0
                print(brake)
        
        stopped = True
        while True:
            
            delta_d = self.__get_d()

            # If we have no value, set speed to 0 as a safety measure

            delta_v = self.__get_delta_v_for_forward_object()
            
            

            c_time = int(time.time())
            if c_time % 3 == 0 and c_time != last_time:
                logging.info("{} : {} suggest speed : {} | d_dist : {} | d_velo : {} | dbg : {}".format(
                    c_time,
                    type(self).__name__,
                    self.speed,
                    delta_d,
                    delta_v,
                    self.debug_string
                ))
                last_time = c_time

            if delta_d is None or delta_v is None:
                self.drive(0)
                continue

            #set true if the car has stopped
            
            
            #delta_d = self.__get_d()
            print(delta_d)
            
            #as long as distance is less than desired distance, keep speed
            if delta_d > set_d: 
                sp = self.wanted_speed
                self.drive(sp)
                delta_d = self.__get_d()
                '''
                With the new distance, yet again check if the distance is larger than desired distance. 
                Set stopped to False as the car is ready to self.drive
                '''
                if delta_d > set_d:
                    stopped = False
                    #time.sleep(0.1)
                print(delta_d)
            '''
            if distance is smaller than desired distance, brake.
            we have several different brake functions, depending on whether aggressive braking is needed or not
            for aggressive braking electric brake is used, for less aggressive brake use decremental brake.
            distance based brake aims to keep the set_d to the car in front
            Electric brake runs the risk of stalling and reversing. Therefore using it only allows for braking
            when distance is larger than 10 cm.
            '''
            if 0 < delta_d < set_d:
                #delta_d = self.__get_d()
                
                if brake == 0:
                    if not stopped:
                        if delta_d < set_d/2: #added
                            self.electric_braking()
                        else: #added
                            self.mod_electric_braking() #added
                        
                        print(delta_d)
                        if delta_d < 10: #Changed from 0.05 to 0.1
                            stopped = True
                            self.drive(0)
                elif brake == 1:
                    self.distance_based_brake(set_d)
                elif brake == 2:
                    self.decremental_brake(sp)
                else:
                    sp = 0
                    self.drive(sp)
                    
                    print(delta_d)

    def electric_braking(self):
        for x in range(0, 10):
            #Decrease this to improve braking. Might lead to stalling
            self.drive(-100)
    '''
    Slower electric brake. To avoid stopping completely
    '''
    def mod_electric_braking(self):
        for x in range(0, 10):
            #Decrease this to improve braking. Might lead to stalling
            self.drive(-20)
    
    def decremental_brake(self, sp):
        for x in range(0,sp):
            self.drive(sp - (x + 1))

    def distance_based_brake(self, set_d):
        delta_d = self.__get_d()
        if delta_d < set_d:
            sp = self.core.speed
            while sp > 0:
                sp -= 5
                if sp < 0:
                    sp = 0
                self.drive(sp)
                
    def drive(self, sp):
        self.speed = sp
    
    def __change_speed(self, delta_v):
        delta_v = float(delta_v)
        self.__set_speed(delta_v + self.current_speed)

    def __set_speed(self, speed):
        # Should prevent MOPED from backing when "braking" at current speed = 0

        if self.current_speed is 0 and speed < 0:
            self.speed = 0
        else:
            if abs(speed) > self.wanted_speed:
                if speed < 0:
                    self.speed = -self.wanted_speed
                else:
                    self.speed = self.wanted_speed
            else:
                self.speed =speed

    # Gets distance to preceding vehicle, if not more than 2
    def __get_d(self):
        if len(self.core.get_ultra_data()) == 0:
            return None

        try:
            (timestamp, dist) = self.core.get_ultra_data()[0]
        except IndexError:
            return None  # None values are handled in the loop

        if len(self.distance_time_list) is 0:
            self.__update_lists(timestamp, dist)
        elif timestamp != self.distance_time_list[-1]:
            self.__update_lists(timestamp, dist)

        return self.__get_average_of(self.distance_list)

    def __update_lists(self, timestamp, dist):
        self.distance_list.append(min(dist, self.DISTANCE_CAP_CENTIMETRES))
        self.distance_time_list.append(timestamp)

        self.__check_timestamp_validity()

    def __check_timestamp_validity(self):
        while time.clock() - self.distance_time_list[0] > self.DIST_DATA_LIFETIME:
            self.distance_list = self.distance_list[1:]
            self.distance_time_list = self.distance_time_list[1:]

    # Approximates the difference in speed to
    # the target by using constructing a
    # linear function from two (distance, time) points
    def __get_delta_v_for_forward_object(self):
        size = len(self.distance_list)
        if not size:
            return

        # values to determine the size of the slices from the data list
        half_point_ceiled = ceil(size / 2)
        half_point_floored = floor(size / 2)
        if half_point_ceiled == half_point_floored:
            half_point_floored -= 1

        # The point p0
        d0 = self.__get_average_of(self.distance_list[half_point_ceiled:])
        t0 = self.__get_average_of(self.distance_time_list[half_point_ceiled:])

        # The point p1
        d1 = self.__get_average_of(self.distance_list[:half_point_floored])
        t1 = self.__get_average_of(self.distance_time_list[:half_point_floored])

        # The incline between p0 and p1 is the relative speed
        delta_d = d1 - d0
        delta_t = t1 - t0

        if delta_d is 0 or delta_t is 0:
            return None

        return delta_d / delta_t

    def __get_average_of(self, my_list):
        if not len(my_list):
            return 0  # see no evil

        avg = 0
        for val in my_list:
            avg = avg + val
        avg = avg / len(my_list)
        return avg
