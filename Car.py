import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Car():
	'''
	y:   lateral displacement
	v:   lateral velocity
	psi: heading angle
	r:   angular velocity
	'''
	def __init__(self, y, v, psi, r):
		self.m = 100
		self.Cf = 5
		self.Cr = 5
		self.Lf = 2
		self.Lr = 2
		self.Iz = 10
		self.u0 = 3

		self.y = y
		self.v = v
		self.psi = psi
		self.r = r

		self.t = 0

		self.cx = 0
		self.cy = 0

		carWidth = 30
		carLength = 60

		self.chassis = np.zeros((5,2))
		self.chassisRef = np.zeros((5,2))
		self.chassisRef[0,0] = -carLength/2
		self.chassisRef[1,0] = -carLength/2
		self.chassisRef[2,0] = carLength/2
		self.chassisRef[3,0] = carLength/2
		self.chassisRef[4,0] = -carLength/2
		self.chassisRef[0,1] = -carWidth/2
		self.chassisRef[1,1] = carWidth/2
		self.chassisRef[2,1] = carWidth/2
		self.chassisRef[3,1] = -carWidth/2
		self.chassisRef[4,1] = -carWidth/2

	def update(self, delta, dt=1):
		A = np.zeros((4,4))
		B = np.zeros((4,1))
		X = np.zeros((4,1))
		U = np.zeros((1,1))

		A[0,1] = 1
		A[1,1] = -(self.Cf+self.Cr)/(self.m*self.u0)
		A[3,1] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.Iz*self.u0)
		A[0,2] = self.u0
		A[1,3] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.m*self.u0)-self.u0
		A[2,3] = 1
		A[3,3] = -(self.Cf*self.Lf*self.Lf+self.Cr*self.Lr*self.Lr)/(self.Iz*self.u0)

		B[1,0] = self.Cf/self.m
		B[3,0] = self.Cf*self.Lf/self.Iz

		X[0,0] = self.y
		X[1,0] = self.v
		X[2,0] = self.psi
		X[3,0] = self.r

		U[0,0] = delta

		result = dt*np.matmul(A,X)+np.matmul(B,U)

		self.y += result[0,0]
		self.v += result[1,0]
		self.psi += result[2,0]
		self.r += result[3,0]

		X[0,0] = self.y
		X[1,0] = self.v
		X[2,0] = self.psi
		X[3,0] = self.r

		rotMatrix = np.array([[math.cos(self.psi),math.sin(self.psi)],[-1*math.sin(self.psi),math.cos(self.psi)]])
		movementVector = np.matmul(np.array([self.u0,self.v]).T,rotMatrix)
		positionVector = np.array([self.cx,self.cy]).T + movementVector
		self.cx = positionVector[0]
		self.cy = positionVector[1]

		self.chassis = np.matmul(self.chassisRef,rotMatrix) + positionVector

	def plot(self,ax):
		ax.scatter(self.cx, self.cy,100,'k',zorder=1)

def animate(t):
	car.update(0.1) # Steering
	xdata.append(car.cx)
	ydata.append(car.cy)
	particle.set_data(car.cx,car.cy)
	path.set_data(xdata,ydata)
	#direction.set_data([car.cx,car.cx+50*math.cos(car.psi)],[car.cy,car.cy+50*math.sin(car.psi)])
	chassis.set_data(car.chassis[:,0], car.chassis[:,1])
	return particle,path,direction,chassis

car = Car(0,0,0,0)

fig = plt.figure()
ax = plt.subplot()

xdata,ydata = [],[]
particle, = ax.plot([], [],'ko')
path, = ax.plot([],[],'b--',zorder=1)
direction, = ax.plot([],[],'k-')
chassis, = ax.plot([],[],'r-')
ax.set_xlim([-250,250])
ax.set_ylim([-250,250])
ax.set_aspect('equal')
ax.grid()
plt.tight_layout()


anim = animation.FuncAnimation(fig, animate,
	#frames = 10,
	interval = 10,
	blit = True)

plt.show()




