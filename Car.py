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
		self.Cf = 1
		self.Cr = 1
		self.Lf = 2
		self.Lr = 2
		self.Iz = 100
		self.u0 = 2

		self.y = y
		self.v = v
		self.psi = psi
		self.r = r

		self.t = 0

		self.cx = 0
		self.cy = 0

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

		rotMatrix = np.array([[math.cos(self.psi),-1*math.sin(self.psi)],[math.sin(self.psi),math.cos(self.psi)]])
		movementVector = np.matmul(np.array([self.u0,self.v]).T,rotMatrix)
		positionVector = np.array([self.cx,self.cy]).T + movementVector
		self.cx = positionVector[0]
		self.cy = positionVector[1]

		print(positionVector)

	def plot(self,ax):
		ax.scatter(self.cx, self.cy,100,'k',zorder=1)

def animate(t):
	car.update(0.1*math.sin(t*0.01)) # Steering
	xdata.append(car.cx)
	ydata.append(car.cy)
	particle.set_data(car.cx,car.cy)
	path.set_data(xdata,ydata)
	return particle,path

car = Car(0,0,0,0)

fig = plt.figure()
ax = plt.subplot()

xdata,ydata = [],[]
particle, = ax.plot([], [],'ko')
path, = ax.plot([],[],'b--',zorder=1)
ax.set_xlim([-1000,1000])
ax.set_ylim([-1000,1000])
ax.set_aspect('equal')
ax.grid()
plt.tight_layout()


anim = animation.FuncAnimation(fig, animate,
	#frames = 10,
	interval = 10,
	blit = True)

plt.show()




