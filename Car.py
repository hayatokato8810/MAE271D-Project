import math
import numpy as np
import matplotlib.pyplot as plt

class Car():
	'''
	y:	 lateral displacement
	v:	 lateral velocity
	psi: heading angle
	r:	 angular velocity
	'''
	def __init__(self, y, v, psi, r):
		self.m = 100
		self.Cf = 1
		self.Cr = 1
		self.Lf = 2
		self.Lr = 2
		self.Iz = 10
		self.u0 = 1

		self.y = y
		self.v = v
		self.psi = psi
		self.r = r

	def update(self, delta):
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

		result = np.matmul(A,X)+np.matmul(B,U)

		self.y += result[0,0]
		self.v += result[1,0]
		self.psi += result[2,0]
		self.r += result[3,0]

		X[0,0] = self.y
		X[1,0] = self.v
		X[2,0] = self.psi
		X[3,0] = self.r
		print(X)

def main():
	print("Starting")

	#fig = plt.figure()
	#ax = plt.subplot()

	car = Car(-50,1,0,0)
	while True:
		car.update(0)
		input()


if __name__ == '__main__':
	main()
