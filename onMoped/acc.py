import time

# update_time = 0.1
# acceleration_interval = 10
# limit_d = 2
# sigma_v = 2
# sigma_d = 0.1
# sleep_time = 0.00001

# BREAKING_CONSTANT_METRES = 2
# ACCELERATE_STEPS = 5
# MIN_SPEED = 10
# START_SPEED = 20




# adjust speed according to distance to preceding vehicle, to match its speed
# def activate_acc(set_d):
# 	g.limitspeed=None
# 	sp = 0
# 	while True:
# 		d = g.can_ultra
# 		if d > set_d:
# 			sp = min(sp+1,50)
# 			drive(sp)
# 			time.sleep(sleep_time)
# #			d = g.can_ultra
# 		if d < set_d:
# 			sp = max(sp-5,0)
# 			drive(sp)
# 			time.sleep(sleep_time)
# #			d = g.can_ultra
# 		print("Distance, speed: ", d, ",", sp)
#
# def on():
# 	sp = 0
# 	drive(sp)
# 	while True:
# #		time.sleep(0.2)
# 		d = g.can_ultra
# 		if d > 0.5:
# 			if sp<0:
# 				drive(0)
# 				print("Sign changed (- to +)")
# 			sp = 50
# 			drive(sp)
# 		if d < 0.5:
# 			if sp>0:
# 				drive(0)
# 				print("Sign changed (+ to -)")
# 			sp = -50
# 			drive(sp)
# 		print("Distance, speed: ", d, ", ", sp)
from _thread import start_new_thread
from math import ceil, floor


class Acc():
    LIST_SIZE = 20
    DISTANCE_CAP = 3
    SAFE_DISTANCE = 100
    WANTED_DISTANCE = 150
    DECELERATION_RATIO = 1 / 25
    ACCELERATION_RATIO = 1 / 50
    MAX_TIME_PASSED = 0.5

    def __init__(self, core):
        self.distance_list = []
        self.distance_time_list = []
        self.core = core
        self.speed = 0
        self.wanted_speed = 0

        start_new_thread(self.__acc_on, ())

    def __acc_on(self):
        print("started acc_on")

        last_time = time.time()

        while True:

            c_time = int(time.time())
            if c_time % 3 == 0 and c_time != last_time:
                print(str(c_time) + ': ' + type(self).__name__ + ' suggest driving at ' + str(self.speed))  # usch
                last_time = c_time

            delta_d = self.__get_d()
            if delta_d is None:
                continue
            # print("delta_d = " + '%.2f' % delta_d)
            delta_v = self.__get_delta_v_for_forward_object()

            if delta_d >= self.DISTANCE_CAP:
                # in case of no obstacles, go for desired speed
                if self.core.speed != self.wanted_speed:
                    self.speed = self.wanted_speed
            elif delta_d < self.SAFE_DISTANCE:  # decrease speed if too close to target
                self.__change_speed(-1 + (delta_d - self.SAFE_DISTANCE) * self.DECELERATION_RATIO)
            elif delta_d > self.WANTED_DISTANCE:  # increase speed if too far away from target
                self.__change_speed(1 + (delta_d - self.WANTED_DISTANCE) * self.ACCELERATION_RATIO)
            elif delta_v < 0:  # decrease speed if moving too fast relative to target
                self.__change_speed(delta_v)
            elif delta_v > 0:  # increase speed if too slow relative to target
                self.__change_speed(delta_v)

    def __change_speed(self, delta_v):
        output = self.core.speed
        self.speed = output + delta_v

    # Gets distance to preceding vehicle, if not more than 2
    def __get_d(self):
        try:
            (timestamp, dist) = self.core.get_ultra_data()
            if timestamp != self.distance_time_list[-1]:
                self.distance_list.append(min(dist, self.DISTANCE_CAP))
                self.distance_time_list.append(timestamp)

                size = len(self.distance_list)
                self.__check_timestamp_validity()

            return self.__get_average_of(self.distance_list) * 100
        except ValueError as msg:
            return None

    def __check_timestamp_validity(self):
        while time.clock() - self.distance_time_list[0] > self.MAX_TIME_PASSED:
            self.distance_list = self.distance_list[1:]
            self.distance_time_list = self.distance_time_list[1:]

    '''
    Approximates the difference in speed to
    the target by using constructing a 
    linear function from two (distance, time) points
    '''

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
        return delta_d * 100 / delta_t

    def __get_average_of(self, my_list):
        if not len(my_list):
            return 0  # see no evil

        avg = 0
        for val in my_list:
            avg = avg + val
        avg / len(my_list)
        return avg
