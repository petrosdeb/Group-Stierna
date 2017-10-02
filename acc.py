# Crude attempt at acc implementation, for testing purposes.
import time
from driving import drive
from nav import *

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


