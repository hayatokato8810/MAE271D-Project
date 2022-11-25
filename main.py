import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Car
import Track

def animate(time,ax):
	global car,track

	plt.cla()
	car.update(1,0.001)
	track.plot(ax)
	car.plot(ax)

	#d,closept = track.proximity(car.pos())
	#print(closept)

	d = track.distanceTo(car.pos())

	c1 = plt.Circle(car.pos(),d,edgecolor='k',alpha=0.1)
	ax.add_patch(c1)

	#ax.plot([car.cx,closept[0]],[car.cy,closept[1]])
	
	#ax.plot([car.cx,closept[0,0]],[car.cy,closept[0,1]])
	#ax.plot([car.cx,closept[1,0]],[car.cy,closept[1,1]])
	#ax.plot([car.cx,closept[2,0]],[car.cy,closept[2,1]])
	
	#ax.set_xlim([-10,20])
	#ax.set_ylim([-5,10])

	scale = 3
	ax.set_xlim([car.cx-scale,car.cx+scale])
	ax.set_ylim([car.cy-scale,car.cy+scale])

	ax.set_aspect('equal')
	ax.grid()

def main():
	global car,track

	fig = plt.figure()
	ax = plt.subplot()

	car = Car.Car(0,0,0,0)
	center, inner, outer = Track.loadTrackData('1.npy')
	track = Track.Track(center, inner, outer)

	anim = animation.FuncAnimation(fig, animate, fargs = (ax,), interval = 200)

	plt.show()

if __name__ == '__main__':
	main()