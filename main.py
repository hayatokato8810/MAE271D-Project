import math
import quaternion
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import Car
import Track

Kp = 10
Kd = 10
prevErr = 0
deltaErr = 0
T = 10

def animate(time,ax):
	global car,track,prevErr
	d,point,heading = track.closestRef(car.pos())
	v1 = np.array(car.dir())
	v2 = point - car.pos()
	angle = math.atan2(v1[0]*v2[1]-v1[1]*v2[0],v1[0]*v2[0]+v1[1]*v2[1])

	refTraj = track.refTraj(car.pos(),T+1)
	#print(refTraj[0,0])

	err = d*np.sign(angle)
	deltaErr = err - prevErr
	#print(prevErr - err)
	prevErr = err

	V = 0.1
	dt = 1
	L = 0.4
	lr = 0.2

	A = np.zeros((4,4))
	A[0,0] = 1
	A[1,1] = 1
	A[2,2] = 1
	A[3,3] = 1
	A[1,2] = V*dt
	A[1,3] = V*dt

	B = np.zeros((4,1))
	B[2,0] = V/L*dt
	B[3,0] = lr/L*dt

	C = np.zeros((4))
	C[0] = V*dt

	X = np.zeros((4,1))
	X[0,0] = car.cx
	X[1,0] = car.cy
	X[2,0] = car.psi
	X[3,0] = car.r
	nX,U = car.MPC.optimizeLinearModel(A, B, C, X, refTraj, T)
	print(nX.value[:,0], U.value[0,0])

	#print(car.r)

	plt.cla()
	car.update(2)
	track.plot(ax)
	car.plot(ax)

	#ax.plot(refTraj[0,:],refTraj[1,:],lw=5,solid_capstyle='round')
	'''
	for i in range(T):
		angle = refTraj[2,i]
		scale = 5
		#ax.plot([refTraj[0,i],refTraj[0,i]+scale*math.cos(angle)],[refTraj[1,i],refTraj[1,i]+scale*math.sin(angle)])
	'''

	px = nX.value[0,:]
	py = nX.value[1,:]
	#ax.plot(px,py,'.',zorder=-1)
	#d,closept = track.proximity(car.pos())
	#print(closept)


	c1 = plt.Circle(car.pos(),d,edgecolor='k',alpha=0.1)
	ax.add_patch(c1)

	#ax.plot([car.pos()[0],point[0]],[car.pos()[1],point[1]],'--',zorder=2)

	#ax.plot([car.pos()[0],car.pos()[0]+heading[0]],[car.pos()[1],car.pos()[1]+heading[1]])

	#ax.set_xlim([-10,30])
	#ax.set_ylim([-5,20])

	scale = 5
	ax.set_xlim([car.cx-scale,car.cx+scale])
	ax.set_ylim([car.cy-scale,car.cy+scale])

	ax.set_aspect('equal')
	ax.grid()

def main():
	global car,track

	fig = plt.figure()
	ax = plt.subplot()

	car = Car.Car(0,0,0,0,0.1)
	center, inner, outer = Track.loadTrackData('1.npy')
	track = Track.Track(center, inner, outer)

	anim = animation.FuncAnimation(fig, animate, fargs = (ax,), interval = 20)
	#for i in range(10):
	#	animate(i,ax)
	plt.show()

if __name__ == '__main__':
	main()