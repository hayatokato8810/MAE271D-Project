import math
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

class Track(object):
	def __init__(self, center, width):
		self.width = width

		self.center = center
		self.next = np.roll(self.center,-1,axis=0)

		self.heading = np.divide(self.next - self.center, np.linalg.norm(self.next - self.center,axis=1).reshape((len(self.center),1)))
		self.nextHeading = np.roll(self.heading,-1,axis=0)

		self.angularV = np.zeros((len(self.center),1))
		for i in range(len(self.center)):
			v1 = self.heading[i]
			v2 = self.nextHeading[i]
			self.angularV[i] = math.atan2(v1[0]*v2[1]-v1[1]*v2[0],v1[0]*v2[0]+v1[1]*v2[1])

		self.angle = np.zeros((len(self.center),1))
		prevAngle = 0
		for i in range(len(self.center)):
			self.angle[i] =  prevAngle + self.angularV[i]
			prevAngle = self.angle[i]

	def convertFrame(self, tM, rM):
		center = (self.center - tM)@rM.T
		return center

	def loadTrackData(trackFileName:str):
		return np.load(trackFileName)[:,0:2]

	def closestRef(self, currentPos):
		#center = self.convertFrame(tMatrix, a)
		d, idx = spatial.KDTree(self.center).query(currentPos,k=2)

		closept = self.center[idx]
		p1 = np.array(closept[0])
		p2 = np.array(closept[1])
		p3 = np.array(currentPos)
		l2 = np.sum((p1-p2)**2)
		t = max(0, min(1, np.sum((p3 - p1) * (p2 - p1)) / l2))
		proj = p1 + t * (p2 - p1)

		pt = self.heading[idx[0]]
		tM = proj
		rM = np.array([[pt[0],pt[1]],[-pt[1],pt[0]]])
		return tM,rM

	def refTraj(self, T):
		#center = self.convertFrame(tMatrix, a)
		d, idx = spatial.KDTree(self.center).query(np.zeros(2),k=1)
		traj = np.zeros((4,T))
		traj[0,:] = np.roll(self.center,-idx,axis=0)[:T,0]
		traj[1,:] = np.roll(self.center,-idx,axis=0)[:T,1]

		traj[2,:] = np.roll(self.angle,-idx,axis=0)[:,0][:T]
		traj[3,:] = np.roll(self.angularV,-idx,axis=0)[:,0][:T]
		return traj

	def plot(self,ax):
		cx = np.append(self.center[:,0],self.center[0,0])
		cy = np.append(self.center[:,1],self.center[0,1])
		center, = ax.plot(cx,cy,'--',color='k')



