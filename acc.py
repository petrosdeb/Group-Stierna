import time
import math
from driving import drive
from nav import *


update_time = 0.1
acceleration_interval = 10
limit_d = 2
sigma_v = 2
sigma_d = 0.1
acc_state = True
sleep_time = 0.00001

BREAKING_CONSTANT_METRES = 2
ACCELERATE_STEPS = 5
MIN_SPEED = 10
START_SPEED = 20

delta_v = 0

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


def set_acc_state(state):
	acc_state = state

def acc_on(v_wish):
	while acc_state:
		# g.limitspeed=None

		v_actual = g.outspeedcm/2
		v_wish_delta = v_wish - v_actual
		d_other = get_d()
		d_ok = calculate_break_distance(v_actual)

		if not is_ok_distance(v_actual, d_other):
			adapt_distance(d_other, d_ok, v_actual)

		elif v_wish_delta < 0:
			dv = v_wish_delta
			brake(adapt_velocity(v_actual, dv))
			#drive(adapt_velocity(v_actual, dv))

		elif v_actual < MIN_SPEED and d_other > d_ok and v_wish > 0:
			drive(START_SPEED)

		elif v_wish_delta > 0:
			dv = v_wish_delta/ACCELERATE_STEPS
			if is_ok_distance(v_actual + dv, d_other):
				# drive(v_actual + dv)
				drive(adapt_velocity(v_actual, dv))

		# time.sleep(0.1)

def adapt_velocity(v, dv):
	s = v + dv
	if s <= MIN_SPEED and s > MIN_SPEED/2:
		return MIN_SPEED
	elif s <= MIN_SPEED/2:
		return 0
	else:
		if s < 0:
			s = 0
		return s

def brake(v):
	# drive(-10)
	# time.sleep(sleep_time)
	drive(v)

# def stop():
# 	drive(0)

def adapt_distance(d1, d2, v):
	d_delta = d1 - d2
	v_delta = get_delta_v(d_delta)
	dv = v_delta/ACCELERATE_STEPS
	s = v + dv
	if v <= 0:
		s = 0
	drive(s)

def is_ok_distance(v, d):
	d_ok = calculate_break_distance(v)
	return d > d_ok

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
def get_d(): # TODO: Get average of eg 20 data points
	d = min(g.can_ultra, 2)
	return d*100

# Calculates difference in speed of preceding vehicle compared to MOPED
def get_delta_v(delta_d):
	delta_v = delta_d/update_time
	return delta_v

# Calculates accepted break distance according to given speed
def calculate_break_distance(sp):
	if sp >= 0:
		break_distance = 0.06*(sp**1.6)
	elif sp < 0:
		break_distance = -0.06*((-sp)**1.6)
	return break_distance + 100 * BREAKING_CONSTANT_METRES

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



