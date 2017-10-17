import time
import math
from acc_can_interface import AccCanInterface
from driving import drive
from nav import *


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

class Acc():
    LIST_SIZE = 20
    DISTANCE_CAP = 3
    SAFE_DISTANCE = 100
    WANTED_DISTANCE = 150
    DECELERATION_RATIO = 1 / 25
    ACCELERATION_RATIO = 1 / 50

    def __init__(self):
        self.distance_list = []
        self.distance_time_list = []
        self.acc_can_interface = None
        self.listener = None

    def acc_on(self, v_wish):
        self.acc_can_interface = AccCanInterface()
        self.listener = self.acc_can_interface.get_listener()
        while True:
            # g.limitspeed=None


            # v_actual = g.outspeedcm/2 # TODO Exchange for actual measurements for actual speed
            # v_wish_delta = v_wish - v_actual
            delta_d = self.get_d()
            print("delta_d = " + '%.2f' % delta_d)
            delta_v = self.get_delta_v_for_forward_object()
            # d_ok = calculate_break_distance(v_actual)

            if delta_d >= self.DISTANCE_CAP:
                # in case of no obstacles, go for desired speed
                if g.outspeedcm / 2 != v_wish:  # TODO
                    drive(v_wish)
            elif delta_d < self.SAFE_DISTANCE:  # decrease speed if too close to target
                self.change_speed(-1 + (delta_d - self.SAFE_DISTANCE) * self.DECELERATION_RATIO)
            elif delta_d > self.WANTED_DISTANCE:  # increase speed if too far away from target
                self.change_speed(1 + (delta_d - self.WANTED_DISTANCE) * self.ACCELERATION_RATIO)
            elif delta_v < 0:  # decrease speed if moving too fast relative to target
                self.change_speed(delta_v)
            elif delta_v > 0:  # increase speed if too slow relative to target
                self.change_speed(delta_v)

                # if not is_ok_distance(v_actual, d_other):
                #     adapt_distance(d_other, d_ok, v_actual)
                #
                # elif v_wish_delta < 0:
                #     brake(adapt_velocity(v_actual, v_wish_delta))
                #     # drive(adapt_velocity(v_actual, dv))
                #
                # elif v_actual < MIN_SPEED and d_other > d_ok and v_wish > 0:
                #     drive(START_SPEED)
                #
                # elif v_wish_delta > 0:
                #     dv = v_wish_delta/ACCELERATE_STEPS
                #     if is_ok_distance(v_actual + dv, d_other):
                #         # drive(v_actual + dv)
                #         drive(adapt_velocity(v_actual, dv))

                # time.sleep(0.1)

    # def adapt_velocity(v, dv):
    #     s = v + dv
    #     if MIN_SPEED >= abs(s) > MIN_SPEED / 2:
    #         return MIN_SPEED * s / abs(s)
    #     elif MIN_SPEED / 2 >= abs(s) >= 0:
    #         return 0
    #     else:
    #         # if s < 0:
    #         # 	s = 0
    #         return s


    def change_speed(self, delta_v):
        # drive(-10)
        # time.sleep(sleep_time)
        output = g.outspeedcm / 2
        drive(output + delta_v)

    # def stop():
    # 	drive(0)

    # def adapt_distance(d1, d2, v):
    #     d_delta = d1 - d2
    #     v_delta = get_delta_v(d_delta)
    #     dv = v_delta / ACCELERATE_STEPS
    #     s = v + dv
    #     if v <= 0:
    #         s = 0
    #     drive(s)


    # def is_ok_distance(v, d):
    #     d_ok = calculate_break_distance(v)
    #     return d > d_ok


    # Behaviour for Adaptive Cruise Control (ACC). set_sp is desired speed to be maintained.
    # def acc(set_sp):
    # 	max_speed = set_sp
    # 	max_d = calculate_break_distance(max_speed)
    # 	while True:
    # 		v = g.outspeedcm/2  # last input to drive()
    # 		acceleration_speed = (max_speed-v)/acceleration_interval  # accelerate with intervals
    # 		while is_outside_break_distance(max_d) and v < max_speed:
    # 			accelerate(acceleration_speed)
    # 			v = g.outspeedcm/2
    # 		if not is_outside_break_distance(max_d):
    # 			v = g.outspeedcm/2
    # 			preceding_v = calculate_preceding_speed(v)
    # 			break_distance = calculate_break_distance(preceding_v)
    # 			acceleration_speed = (preceding_v-v)/acceleration_interval
    # 			if is_outside_break_distance(break_distance) and is_match_speed(preceding_v):
    # 				drive(v)
    # 			else:
    # 				while not is_outside_break_distance(break_distance) and is_match_speed(preceding_v):
    # 					adjust_distance(break_distance)
    # 				while not is_match_speed(preceding_v):
    # 					accelerate(acceleration_speed)
    # 					v = g.outspeedcm/2

    # Divide delta_v into even pieces, add these to current speed
    # def accelerate(v_actual, dv):
    # 	v = g.outspeedcm/2 # Current speed
    # 	drive(v+delta_v)

    # Gets difference in distance to preceding vehicle given a time
    # def get_delta_d():
    # 	d0 = get_d()
    # 	time.sleep(update_time)
    # 	d1 = get_d()
    # 	return d1-d0

    # Gets distance to preceding vehicle, if not more than 2
    def get_d(self):
        (timestamp, dist) = self.listener.data_fetch(1)
        if timestamp != self.distance_time_list[-1]:
            self.distance_list.append(min(dist, self.DISTANCE_CAP))
            self.distance_time_list.append(timestamp)

            size = len(self.distance_list)
            if size > self.LIST_SIZE:  # TODO Evaluate if this should be based on timestamp instead
                self.distance_list = self.distance_list[size - self.LIST_SIZE: size - 1]
                self.distance_time_list = self.distance_time_list[size - self.LIST_SIZE: size - 1]

        return self.get_average_of(self.distance_list) * 100
        # return min(g.can_ultra, DISTANCE_CAP) * 100

    def get_delta_v_for_forward_object(self):
        size = len(self.distance_list)

        d0 = self.get_average_of(self.distance_list[size / 2: size - 1])
        d1 = self.get_average_of(self.distance_list[0: size / 2 - 1])

        t0 = self.get_average_of(self.distance_time_list[size / 2: size - 1])
        t1 = self.get_average_of(self.distance_time_list[0: size / 2 - 1])

        delta_d = d1 - d0
        delta_t = t1 - t0
        return delta_d * 100 / delta_t
        # return min(g.can_ultra, DISTANCE_CAP) * 100 / 0.001

    def get_average_of(self, my_list):
        avg = 0
        for val in my_list:
            avg = avg + val
        avg / len(my_list)
        return avg

        # Calculates difference in speed of preceding vehicle compared to MOPED
        # def get_delta_v(delta_d):
        #     delta_v = delta_d / update_time
        #     return delta_v


        # Calculates accepted break distance according to given speed
        # def calculate_break_distance(sp):
        #     if sp >= 0:
        #         break_distance = 0.06 * (sp ** 1.6)
        #     else:
        #         break_distance = -0.06 * ((-sp) ** 1.6)
        #     return break_distance + 100 * BREAKING_CONSTANT_METRES

        # Returns True if MOPED is matching speed to preceding vehicle
        # def is_match_speed(sp):
        # 	v = g.outspeedcm/2
        # 	return sp - sigma_v <= v and v <= sp

        # Returns True if MOPED is outside of break distance to preceding vehicle
        # def is_outside_break_distance(break_distance):
        # 	return get_d() >= break_distance + sigma_d

        # Adjusts speed of vehicle until set distance is kept
        # def adjust_distance(break_distance):
        # 	delta_d = get_d() - break_distance
        # 	delta_v = get_delta_v(delta_d)
        # 	acceleration_speed = delta_v/acceleration_interval
        # 	accelerate(acceleration_speed)

        # Calculates the speed of the preceding vehicle
        # def calculate_preceding_speed(v):
        # 	delta_d = get_delta_d()
        # 	delta_v = get_delta_v(delta_d)
        # 	preceding_v = v + delta_v
        # 	return preceding_v