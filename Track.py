import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

class Track(object):
	def __init__(self, center, inner, outer):
		self.center = center
		self.inner = inner
		self.outer = outer

	def proximity(self,point):
		dist, idx = spatial.KDTree(self.center).query(point,k=2)
		closePoints = self.center[idx]
		avgDist = np.average(dist)

		#diff = abs(dist[0]-dist[1])
		#dist = dist[-1]-dist
		#avgPoint = np.average(closePoints,axis=0,weights = dist)
		#print(diff)

		return dist,closePoints
		#return avgDist, avgPoint

	def distanceTo(self,point):
		d, idx = spatial.KDTree(self.center).query(point,k=2)
		closept = self.center[idx]
		p1 = np.array(closept[0])
		p2 = np.array(closept[1])
		p3 = np.array(point)
		dist = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
		return dist

	def plot(self,ax):
		cx = np.append(self.center[:,0],self.center[0,0])
		cy = np.append(self.center[:,1],self.center[0,1])
		ix = np.append(self.inner[:,0],self.inner[0,0])
		iy = np.append(self.inner[:,1],self.inner[0,1])
		ox = np.append(self.outer[:,0],self.outer[0,0])
		oy = np.append(self.outer[:,1],self.outer[0,1])
		center, = ax.plot(cx,cy,'-',color='k')
		inner, = ax.plot(ix,iy,color='k')
		outer, = ax.plot(ox,oy,color='k')

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

	pt = [10,8.5]
	#d, closept = track.proximity(pt)

	#print(d)

	# Plot
	track.plot(ax)
	#plt.plot([pt[0],closept[0]],[pt[1],closept[1]])

	print(center[0])
	print(center[-1])

	ax.set_aspect('equal')
	ax.grid()
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
