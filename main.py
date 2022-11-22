import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Car
import Track

def animate(time,ax):
	global car,track

	plt.cla()
	car.update(0.5,0.01)
	track.plot(ax)
	car.plot(ax)

	d,closept = track.proximity(car.pos())
	ax.plot([car.cx,closept[0]],[car.cy,closept[1]])

	#ax.set_xlim([-10,20])
	#ax.set_ylim([-5,10])

	scale = 5
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

	anim = animation.FuncAnimation(fig, animate, fargs = (ax,), interval = 20)

	plt.show()

if __name__ == '__main__':
	main()