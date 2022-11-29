import math
import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

class Track(object):
	vector = tuple[float]

	def __init__(self, center, inner, outer):
		self.center = center
		self.inner = inner
		self.outer = outer

		# Removed Duplicate in Data
		self.center = np.delete(self.center,186,axis=0)
		with open('test.npy', 'wb') as f:
			np.save(f, self.center)

		self.next = np.roll(self.center,-1,axis=0)
		heading = self.next - self.center
		self.heading = np.divide(heading, np.linalg.norm(heading,axis=1).reshape((len(self.center),1)))
		self.prevHead = np.roll(self.heading,-1,axis=0)

		self.angularV = np.zeros((len(self.center),1))
		for i in range(len(self.center)):
			v1 = self.heading[i]
			v2 = self.prevHead[i]
			self.angularV[i] = math.atan2(v1[0]*v2[1]-v1[1]*v2[0],v1[0]*v2[0]+v1[1]*v2[1])

		self.angle = np.zeros((len(self.center),1))
		prevAngle = 0
		for i in range(len(self.center)):
			self.angle[i] =  prevAngle + self.angularV[i]
			prevAngle = self.angle[i]

	# Returns the closest reference to the track
	# dist: lateral distance to the closest point on the reference track
	# proj: projected closest point on the reference track
	# head: desired heading at that point on track
	def closestRef(self,point:vector) -> tuple[float, vector, vector]:
		d, idx = spatial.KDTree(self.center).query(point,k=2)
		closept = self.center[idx]
		p1 = np.array(closept[0])
		p2 = np.array(closept[1])
		p3 = np.array(point)
		dist = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

		l2 = np.sum((p1-p2)**2)
		t = max(0, min(1, np.sum((p3 - p1) * (p2 - p1)) / l2))
		proj = p1 + t * (p2 - p1)

		head = 0.5*self.heading[idx[0]] + 0.5*self.heading[idx[1]]

		return dist, proj, head

	def refTraj(self,point:vector, T:int):
		d, idx = spatial.KDTree(self.center).query(point,k=1)
		traj = np.zeros((4,T))
		traj[0,:] = np.roll(self.center,-idx,axis=0)[:T,0]
		traj[1,:] = np.roll(self.center,-idx,axis=0)[:T,1]
		traj[2,:] = np.roll(self.angle,-idx,axis=0)[:,0][:T]
		traj[3,:] = np.roll(self.angularV,-idx,axis=0)[:,0][:T]
		return traj

	def plot(self,ax):
		cx = np.append(self.center[:,0],self.center[0,0])
		cy = np.append(self.center[:,1],self.center[0,1])
		ix = np.append(self.inner[:,0],self.inner[0,0])
		iy = np.append(self.inner[:,1],self.inner[0,1])
		ox = np.append(self.outer[:,0],self.outer[0,0])
		oy = np.append(self.outer[:,1],self.outer[0,1])
		center, = ax.plot(cx,cy,'--',color='k')
		inner, = ax.plot(ix,iy,color='k')
		outer, = ax.plot(ox,oy,color='k')
		#for i in range(len(self.center)):
		#	angle =  self.angle[i]
		#	ax.plot([self.center[i,0],self.center[i,0]+0.5*math.cos(angle)],[self.center[i,1],self.center[i,1]+0.5*math.sin(angle)])
			
		'''
		prevAngle = self.angle[len(self.center)-1]
		for i in range(len(self.center)):
			angle =  prevAngle + self.angle[i]
			ax.plot([self.center[i,0],self.center[i,0]+0.5*math.cos(angle)],[self.center[i,1],self.center[i,1]+0.5*math.sin(angle)])
			prevAngle = angle
		'''

def loadTrackData(trackFileName:str):
	data = np.load("./tracks/" + trackFileName)
	center = data[:-1,0:2]
	inner  = data[:-1,2:4]
	outer  = data[:-1,4:6]
	return center,inner,outer

def main():

	fig = plt.figure()
	ax = plt.subplot()

	center, inner, outer = loadTrackData('1.npy')
	track = Track(center, inner, outer)

	# Plot
	track.plot(ax)

	ax.set_aspect('equal')
	ax.grid()
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
