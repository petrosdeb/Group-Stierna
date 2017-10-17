# Crude attempt at acc implementation, for testing purposes.
from driving import drive
from nav import *
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


def act_acc(set_d):
	while True:
		d = g.can_ultra
		print(d)
		while d > set_d:
			sp = 15
			drive(sp)
			d = g.can_ultra
			print(d)
		while d < set_d:
			sp = 0
			drive(sp)
			d = g.can_ultra
			print(d)