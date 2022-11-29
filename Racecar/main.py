import math
import quaternion
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Car import Car
from Track import Track
from MPC import MPC

A = np.zeros((4,4))
B = np.zeros((4,1))
C = np.zeros((4))
T = 10

def main():
	global car,track,mpc
	car = Car(0,0,0,0,0.1)
	track = Track(Track.loadTrackData('test.npy'),5)

	Q = np.diag([10000,10000,10,10])
	R = np.diag([10])
	mpc = MPC(4,1,Q,R)

	fig = plt.figure()
	ax1 = plt.subplot(1,2,1)
	ax2 = plt.subplot(1,2,2)
	ax = (ax1, ax2)

	anim = animation.FuncAnimation(fig, animate, fargs = (ax,), interval = 100)
	#animate(0,ax)

	plt.tight_layout()
	plt.show()

def animate(time, ax):
	global car,track,mpc
	# Update Car

	#print(car.X)
	carPos = car.pos
	tM,rM = track.closestRef(carPos)
	#print(tM,rM)
	newTrack = Track(track.convertFrame(tM,rM),5)
	traj = newTrack.refTraj(T+1)
	newCarPos = (carPos - tM)@rM.T
	newCarVel = car.dir @ rM.T
	#print(newCarVel)

	V = 0.05
	dt = 1
	L = 0.4
	lr = 0.2

	A[0,0] = 1
	A[1,1] = 1
	A[2,2] = 1
	A[3,3] = 1
	A[1,2] = V*dt
	A[1,3] = V*dt

	B[2,0] = V/L*dt
	B[3,0] = lr/L*dt

	C[0] = V*dt

	X = np.zeros((4,1))
	X[0,0] = 0
	X[1,0] = newCarPos[1]
	X[2,0] = car.X[2,0]
	X[3,0] = car.X[3,0]
	newX,U = mpc.optimizeLinearModel(A, B, C, X, traj, T)
	car.update(U.value[0,0])

	print(U.value[0,0])


	# Plot
	ax1,ax2 = ax
	ax1.cla()
	ax2.cla()
	
	track.plot(ax1)
	#ax1.plot(carPos[0],carPos[1],'o')
	ax1.plot([tM[0],tM[0] + rM[0,0]],[tM[1],tM[1] + rM[0,1]],'r-',zorder=3)
	ax1.plot([tM[0],tM[0] + rM[1,0]],[tM[1],tM[1] + rM[1,1]],'g-',zorder=3)
	car.plot(ax1)

	newTrack.plot(ax2)
	ax2.plot(0,newCarPos[1],'o')
	ax2.plot([0,1],[0,0],'r-',zorder=3)
	ax2.plot([0,0],[0,1],'g-',zorder=3)
	ax2.plot(traj[0,:],traj[1,:],lw=5,zorder=2)
	px = newX.value[0,:]
	py = newX.value[1,:]
	ax2.plot(px,py,'.',zorder=4)
	ax2.set_xlim([-5,5])
	ax2.set_ylim([-5,5])

	formatPlot(ax1)
	formatPlot(ax2)

def formatPlot(ax):
	ax.set_aspect('equal')
	ax.grid()

if __name__ == '__main__':
	main()