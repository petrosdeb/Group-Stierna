import time
from driving import drive
from nav import *


update_time = 0.1
acceleration_interval = 10
limit_d = 2
sigma_v = 2
sigma_d = 0.1

# adjust speed according to distance to preceding vehicle, to match its speed 
def activate_acc(set_d):
	g.limitspeed=None
	sp = 0
	while True:
		d = g.can_ultra
		if d > set_d:
			sp = min(sp+1,50)
			drive(sp)
			time.sleep(0.00001)
#			d = g.can_ultra
		if d < set_d:
			sp = max(sp-5,0)
			drive(sp)
			time.sleep(0.00001)
#			d = g.can_ultra
		print("Distance, speed: ", d, ",", sp)

def on():
	sp = 0
	drive(sp)
	while True:
#		time.sleep(0.2)
		d = g.can_ultra
		if d > 0.5:
			if sp<0:
				drive(0)
				print("Sign changed (- to +)")
			sp = 50
			drive(sp)
		if d < 0.5:
			if sp>0:
				drive(0)
				print("Sign changed (+ to -)")
			sp = -50
			drive(sp)
		print("Distance, speed: ", d, ", ", sp)

# Behaviour for Adaptive Cruise Control (ACC). set_sp is desired speed to be maintained.
def acc(set_sp):
	max_speed = set_sp
	max_d = calculate_break_distance(max_speed)
	while True:
		v = g.outspeedcm/2  # last input to drive()
		acceleration_speed = (max_speed-v)/acceleration_interval  # accelerate with intervals 
		while is_outside_break_distance(max_d) and v < max_speed:
			accelerate(acceleration_speed)
			v = g.outspeedcm/2
		if not is_outside_break_distance(max_d):
			v = g.outspeedcm/2
			preceding_v = calculate_preceding_speed(v)
			break_distance = calculate_break_distance(preceding_v)
			acceleration_speed = (preceding_v-v)/acceleration_interval
			if is_outside_break_distance(break_distance) and is_match_speed(preceding_v):
				drive(v)
			else:
				while not is_outside_break_distance(break_distance) and is_match_speed(preceding_v):
					adjust_distance(break_distance)
				while not is_match_speed(preceding_v):
					accelerate(acceleration_speed)
					v = g.outspeedcm/2


# Divide delta_v into even pieces, add these to current speed
def accelerate(delta_v):
	v = g.outspeedcm/2 # Current speed
	drive(v+delta_v)
	
# Gets difference in distance to preceding vehicle given a time
def get_delta_d():
	d0 = get_d()
	time.sleep(update_time)
	d1 = get_d()
	return d1-d0

# Gets distance to preceding vehicle, if not more than 2
def get_d():
	d = min(g.can_ultra, 2)
	return d

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
	return break_distance

# Returns True if MOPED is matching speed to preceding vehicle 
def is_match_speed(sp):
	v = g.outspeedcm/2
	return sp - sigma_v <= v and v <= sp

# Returns True if MOPED is outside of break distance to preceding vehicle 
def is_outside_break_distance(break_distance):
	return get_d() >= break_distance + sigma_d

# Adjusts speed of vehicle until set distance is kept
def adjust_distance(break_distance):
	delta_d = get_d() - break_distance
	delta_v = get_delta_v(delta_d)
	acceleration_speed = delta_v/acceleration_interval
	accelerate(acceleration_speed)

# Calculates the speed of the preceding vehicle
def calculate_preceding_speed(v):
	delta_d = get_delta_d()
	delta_v = get_delta_v(delta_d)
	preceding_v = v + delta_v
	return preceding_v



