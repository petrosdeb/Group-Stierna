# Crude attempt at acc implementation, for testing purposes.
import time
from driving import drive
from nav import *

break_distance = {21 : 8,
				  33 : 14,
				  43 : 27,
				  53 : 34,
				  64 : 46,
				  75 : 59,
				  83 : 60,
				  95 : 92,
				  106 : 105}

update_time = 0.1
acceleration_interval = 10
limit_d = 2


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


def acc(set_sp):
	while True:
		max_speed = set_sp
		max_d = calculate_break_distance(max_speed)
		v = g.outspeedcm/2  # last input to drive()
		acceleration_speed = max_speed/acceleration_interval
		while get_d() >= max_d and v < max_speed:
			v = v + acceleration_speed
			accelerate(v)
		if get_d() < max_d:
			delta_d = get_delta_d()
			delta_v = get_delta_v(delta_d, update_time)
			break_distance = calculate_break_distance(v + delta_v)






#divide delta_v into even pieces, add these to current speed
def accelerate(delta_v, v):
	drive(v+delta_v)
	
#Gets difference in distance to preceding vehicle given a time
def get_delta_d():
	d0 = get_d()
	time.sleep(update_time)
	d1 = get_d()
	return d1-d0

#Gets distance to preceding vehicle, if not more than 2
def get_d():
	d = min(g.can_ultra, 2)
	return d

#Calculates speed of preceding vehicle
def get_delta_v(delta_d, t):
	delta_v = delta_d/t
	return delta_v

#Calculates accepted break distance according to given speed
def calculate_break_distance(sp):
	return 0.06*(sp(**1.6))

