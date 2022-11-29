import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from MPC import MPC

__author__ = "Hayato Kato"

class Car(object):
	'''
	y:   lateral displacement
	v:   lateral velocity
	psi: heading angle
	r:   angular velocity
	'''
	def __init__(self, y, v, psi, r, spd):
		# Car Parameters
		self.M  = 100
		self.Cf = 5
		self.Cr = 5
		self.Lf = 0.2
		self.Lr = 0.2
		self.Iz = 10
		self.u0 = spd

		# System State
		self.y = y
		self.v = v
		self.psi = psi
		self.r = r

		self.A, self.B = self.carModel()

		self.cx = 0
		self.cy = 0
		self.dx = 0
		self.dy = 0

		carWidth = 0.1
		carLength = 1

		self.chassis = np.zeros((5,2))
		self.chassisRef = np.zeros((5,2))
		self.chassisRef[0,0] = -self.Lr/2
		self.chassisRef[1,0] = -self.Lr/2
		self.chassisRef[2,0] = self.Lf/2
		self.chassisRef[3,0] = self.Lf/2
		self.chassisRef[4,0] = -self.Lr/2
		self.chassisRef[0,1] = -carWidth/2
		self.chassisRef[1,1] = carWidth/2
		self.chassisRef[2,1] = carWidth/2
		self.chassisRef[3,1] = -carWidth/2
		self.chassisRef[4,1] = -carWidth/2

		Q = np.diag([10,10,0,0])
		R = np.diag([5])
		self.MPC = MPC(4,1,Q,R)

	def computeNextInput(self):
		X = np.zeros((4,1))
		X[0,0] = self.y
		X[1,0] = self.v
		X[2,0] = self.psi
		X[3,0] = self.r

	def carModel(self) -> np.ndarray:
		A = np.zeros((4,4))
		A[0,1] = 1
		A[1,1] = -(self.Cf+self.Cr)/(self.M*self.u0)
		A[3,1] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.Iz*self.u0)
		A[0,2] = self.u0
		A[1,3] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.M*self.u0)-self.u0
		A[2,3] = 1
		A[3,3] = -(self.Cf*self.Lf*self.Lf+self.Cr*self.Lr*self.Lr)/(self.Iz*self.u0)

		B = np.zeros((4,1))
		B[1,0] = self.Cf/self.M
		B[3,0] = self.Cf*self.Lf/self.Iz

		return A,B
		
	def xDot(self, delta, dt=0.001):
		A = self.A
		B = self.B
		X = np.zeros((4,1))
		U = np.zeros((1,1))

		X[0,0] = self.y
		X[1,0] = self.v
		X[2,0] = self.psi
		X[3,0] = self.r

		U[0,0] = delta

		return np.matmul(A,X)+np.matmul(B,U)

	def simulate(self, init, actions):
		T = actions.size
		X = np.zeros((4,T))
		x = init
		for i,a in enumerate(actions):
			result = self.xDot(a)
			x[0] += result[0,0]
			x[1] += dt*result[1,0]
			x[2] += result[2,0]
			x[3] += dt*result[3,0]
			X[:,i] = x
		return X

	def update(self, delta, dt=0.001):
		
		result = self.xDot(delta,dt)

		self.y += result[0,0]
		self.v += dt*result[1,0]
		self.psi += result[2,0]
		self.r += dt*result[3,0]

		rotMatrix = np.array([[math.cos(self.psi),math.sin(self.psi)],[-1*math.sin(self.psi),math.cos(self.psi)]])
		movementVector = np.matmul(np.array([self.u0,self.v]).T,rotMatrix)
		positionVector = np.array([self.cx,self.cy]).T + movementVector
		self.cx = positionVector[0]
		self.cy = positionVector[1]
		self.dx = movementVector[0]
		self.dy = movementVector[1]
		'''

		V = self.u0
		dt = 0.1
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
		X[0,0] = self.cx
		X[1,0] = self.cy
		X[2,0] = self.psi
		X[3,0] = self.r

		U = np.zeros((1,1))
		U[0,0] = delta

		result = A@X + B@U + C
		self.cx = result[0,0]
		self.cy = result[1,0]
		self.psi = result[2,0]
		self.r = result[3,0]
		
		#rotMatrix = np.array([[math.cos(self.psi),math.sin(self.psi)],[-1*math.sin(self.psi),math.cos(self.psi)]])
		#movementVector = np.matmul(np.array([self.u0,self.v]).T,rotMatrix)
		#positionVector = np.array([self.cx,self.cy]).T + movementVector
		'''
		self.chassis = np.matmul(self.chassisRef,rotMatrix) + positionVector

	def plot(self,ax):
		pos, = ax.plot(self.cx,self.cy,'ko')
		chassis, = ax.plot(self.chassis[:,0], self.chassis[:,1],'r-')
		direction, = ax.plot([self.cx,self.cx+2*self.dx],[self.cy,self.cy+2*self.dy],'b')
		#print(pos._animated)
		return pos,chassis,direction

	def pos(self):
		return [self.cx,self.cy]

	def dir(self):
		return [self.dx,self.dy]

def animate(t):
	#plt.cla()
	car.update(1,0.01) # Steering
	car.plot(ax)
	xdata.append(car.cx)
	ydata.append(car.cy)
	particle.set_data(car.cx,car.cy)
	path.set_data(xdata,ydata)
	direction.set_data([car.cx,car.cx+50*math.cos(car.psi)],[car.cy,car.cy+50*math.sin(car.psi)])
	chassis.set_data(car.chassis[:,0], car.chassis[:,1])
	#return particle,path,direction,chassis

	ax.set_xlim([-10,10])
	ax.set_ylim([-10,10])
	ax.set_aspect('equal')
	ax.grid()

	#return chassis, position

def main():
	global car,ax,xdata,ydata,particle,path,direction,chassis

	fig = plt.figure()
	ax = plt.subplot()	

	car = Car(0,0,0,0,0.1)

	xdata,ydata = [],[]
	particle, = ax.plot([], [],'ko')
	path, = ax.plot([],[],'b--',zorder=1)
	direction, = ax.plot([],[],'k-')
	chassis, = ax.plot([],[],'r-')
	ax.set_xlim([-250,250])
	ax.set_ylim([-250,250])

	anim = animation.FuncAnimation(fig, animate,
		#frames = 10,
		interval = 100)

	plt.show()


if __name__ == '__main__':
	main()



