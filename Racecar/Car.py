import math
import numpy as np
import matplotlib.pyplot as plt

class Car(object):
	def __init__(self, 
		lat_pos, 
		lat_vel, 
		rot_pos, 
		rot_vel, 
		speed):
		# Car Parameters
		self.M  = 100
		self.Cf = 5
		self.Cr = 5
		self.Lf = 0.2
		self.Lr = 0.2
		self.Iz = 10
		self.Vx = speed

		# State Space
		self.X = np.zeros((4,1))
		self.X[0,0] = lat_pos
		self.X[1,0] = lat_vel
		self.X[2,0] = rot_pos
		self.X[3,0] = rot_vel
		self.A, self.B = self.carModel()

		self.pos = np.array([10,0])
		self.dir = np.array([0,0])

		# Chassis
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

	def update(self, delta, dt=1):
		result = self.xDot(delta)
		#print(result)
		self.X[0,0] += result[0,0]
		self.X[1,0] += dt*result[1,0]
		self.X[2,0] += result[2,0]
		self.X[3,0] += dt*result[3,0]

		lat_vel = self.X[1,0]
		rot_pos = self.X[2,0]
		rotMatrix = np.array([[math.cos(rot_pos),math.sin(rot_pos)],
													[-1*math.sin(rot_pos),math.cos(rot_pos)]])
		self.dir = np.matmul(np.array([dt*self.Vx,lat_vel]).T,rotMatrix)
		self.pos = self.pos + self.dir
		self.chassis = np.matmul(self.chassisRef,rotMatrix) + self.pos

	def carModel(self):
		A = np.zeros((4,4))
		A[0,1] = 1
		A[1,1] = -(self.Cf+self.Cr)/(self.M*self.Vx)
		A[3,1] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.Iz*self.Vx)
		A[0,2] = self.Vx
		A[1,3] = (-self.Lf*self.Cf+self.Lr*self.Cr)/(self.M*self.Vx)-self.Vx
		A[2,3] = 1
		A[3,3] = -(self.Cf*self.Lf*self.Lf+self.Cr*self.Lr*self.Lr)/(self.Iz*self.Vx)
		B = np.zeros((4,1))
		B[1,0] = self.Cf/self.M
		B[3,0] = self.Cf*self.Lf/self.Iz
		return A,B

	def xDot(self, delta):
		A = self.A
		B = self.B
		X = self.X
		U = np.array([[delta]])

		return np.matmul(A,X) + np.matmul(B,U)

	def plot(self,ax):
		pos, = ax.plot(self.pos[0],self.pos[1],'ko')
		#chassis, = ax.plot(self.chassis[:,0], self.chassis[:,1],'r-')
		direction, = ax.plot([self.pos[0],self.pos[0]+5*self.dir[0]],[self.pos[1],self.pos[1]+5*self.dir[1]],'b')
		



