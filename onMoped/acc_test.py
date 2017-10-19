from driving import drive
from nav import *
import time
# adjust speed according to distance to preceding vehicle, to match its speed 
def activate_acc(set_d):
	while True:
		d = g.can_ultra
		sp = 0
		while d > set_d:
			sp += 1
			drive(sp)
		while d < set_d:
			sp -= 1
			drive(sp)

'''
Working implementation
Our main ACC function
set_d: minimum distance to the preceding MOPED desired, in meters
brake: takes input 0, 1, 2 for different brake methods used. Defaults to 0 if faulty input is given
'''
def act_acc(set_d, brake, speed):
	if brake != (0 or 1 or 2):
		brake = 0
	print(brake)
	#set true if the car has stopped
	stopped = True
	while True:
		d = g.can_ultra
		print(d)
		
		#as long as distance is less than desired distance, keep speed
		while d > set_d: 
			sp = speed
			drive(sp)
			d = g.can_ultra
			'''
			With the new distance, yet again check if the distance is larger than desired distance. 
			Set stopped to False as the car is ready to drive
			'''
			if d > set_d:
				stopped = False
				#time.sleep(0.1)
			print(d)
		'''
		if distance is smaller than desired distance, brake.
		we have several different brake functions, depending on whether aggressive braking is needed or not
		for aggressive braking electric brake is used, for less aggressive brake use decremental brake.
		distance based brake aims to keep the set_d to the car in front
		Electric brake runs the risk of stalling and reversing. Therefore using it only allows for braking
		when distance is larger than 10 cm.
		'''
		while 0 < d < set_d:
			d = g.can_ultra
			
			if brake == 0:
				if not stopped:
					electric_braking()
					print(d)
					if d < 0.05:
						stopped = True
						drive(0)
			elif brake == 1:
				distance_based_brake(set_d)
			elif brake == 2:
				decremental_brake(sp)
			else:
				sp = 0
				drive(sp)
				
				print(d)

def electric_braking():
    for x in range(0, 10):
    	#Decrease this to improve braking. Might lead to stalling
        drive(-100)


def decremental_brake(sp):
	for x in range(0,sp):
		drive(sp - (x + 1))

def distance_based_brake(set_d):
	distance = g.can_ultra
	if distance < set_d:
		speed = g.outspeedcm/2
		while speed > 0:
			speed -= 5
			if speed < 0:
				speed = 0
			drive(speed)
			
			
def acc_speed(speed, set_d):
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
	speed = current_speed + 1
	drive(speed)

def decrease_speed(current_speed):
	speed = current_speed - 1
	drive(speed)