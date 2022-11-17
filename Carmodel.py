import math
import numpy as np
import matplotlib.pyplot as plt

class Car():
	def __init__(self, x, y, theta, phi):
		self.x = x
		self.y = y
		self.theta = theta
		self.phi = phi

		# Visual Parameters
		self.carWidth = 3
		self.carLength = 5
		self.wheelWidth = 0.5
		self.wheelRadius = 0.5

	def plot(self, ax):

		frame = np.zeros((4,2))
		rig = np.zeros((6,2))
		wheel = np.zeros((4,2))
		FLwheel = np.zeros((4,2))
		FRwheel = np.zeros((4,2))
		RLwheel = np.zeros((4,2))
		RRwheel = np.zeros((4,2))
		rotMatrix = np.zeros((2,2))

		frame[0,:] = [self.carWidth/2,self.carLength*7/8]
		frame[1,:] = [-self.carWidth/2,self.carLength*7/8]
		frame[2,:] = [-self.carWidth/2,-self.carLength/8]
		frame[3,:] = [self.carWidth/2,-self.carLength/8]

		rig[0,:] = [-self.carWidth/3,self.carLength*3/4]
		rig[1,:] = [0,self.carLength*3/4]
		rig[2,:] = [self.carWidth/3,self.carLength*3/4]
		rig[3,:] = [-self.carWidth/3,0]
		rig[4,:] = [0,0]
		rig[5,:] = [self.carWidth/3,0]

		wheel[0,:] = [self.wheelWidth/2,self.wheelRadius]
		wheel[1,:] = [self.wheelWidth/2,-self.wheelRadius]
		wheel[2,:] = [-self.wheelWidth/2,-self.wheelRadius]
		wheel[3,:] = [-self.wheelWidth/2,self.wheelRadius]

		rotMatrix[0,0] = math.cos(math.radians(self.phi))
		rotMatrix[1,0] = -math.sin(math.radians(self.phi))
		rotMatrix[0,1] = math.sin(math.radians(self.phi))
		rotMatrix[1,1] = math.cos(math.radians(self.phi))

		FLwheel = np.matmul(wheel,rotMatrix)
		FRwheel = np.matmul(wheel,rotMatrix)

		rotMatrix[0,0] = math.cos(math.radians(self.theta))
		rotMatrix[1,0] = -math.sin(math.radians(self.theta))
		rotMatrix[0,1] = math.sin(math.radians(self.theta))
		rotMatrix[1,1] = math.cos(math.radians(self.theta))

		frame = np.matmul(frame,rotMatrix) + np.array([self.x,self.y])
		rig = np.matmul(rig,rotMatrix) + np.array([self.x,self.y])
		FLwheel = np.matmul(FLwheel,rotMatrix) + rig[0,:]
		FRwheel = np.matmul(FRwheel,rotMatrix) + rig[2,:]
		RLwheel = np.matmul(wheel,rotMatrix) + rig[3,:]
		RRwheel = np.matmul(wheel,rotMatrix) + rig[5,:]

		# Body Shell
		ax.fill(frame[:,0],frame[:,1],facecolor='none',edgecolor='b',lw=2)
		# Wheels
		ax.fill(FLwheel[:,0],FLwheel[:,1],facecolor='grey',edgecolor='k',lw=2)
		ax.fill(FRwheel[:,0],FRwheel[:,1],facecolor='grey',edgecolor='k',lw=2)
		ax.fill(RLwheel[:,0],RLwheel[:,1],facecolor='grey',edgecolor='k',lw=2)
		ax.fill(RRwheel[:,0],RRwheel[:,1],facecolor='grey',edgecolor='k',lw=2)
		# Body Reference Frame
		ax.plot([self.x,self.x + 1*math.cos(math.radians(self.theta+90))],
						[self.y,self.y + 1*math.sin(math.radians(self.theta+90))],
						color='red',lw=3,zorder=0)
		ax.plot([self.x,self.x + 1*math.cos(math.radians(self.theta-180))],
						[self.y,self.y + 1*math.sin(math.radians(self.theta-180))],
						color='green',lw=3,zorder=0)
		# Chassis
		ax.plot(rig[0:3,0],rig[0:3,1],'k--',zorder=-1)
		ax.plot(rig[[1,4],0],rig[[1,4],1],'k--',zorder=-1)
		ax.plot(rig[3:6,0],rig[3:6,1],'k--',zorder=-1)
		# Center Dot
		ax.scatter(self.x, self.y,100,'k',zorder=1)

def main():
	print("Starting")

	fig = plt.figure()
	ax = plt.subplot()

	c = Car(10,0,10,-20)
	c.plot(ax)


	ax.set_aspect('equal')
	plt.tight_layout()
	plt.show()
	plt.show()




if __name__ == '__main__':
	main()