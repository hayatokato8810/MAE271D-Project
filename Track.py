import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt

class Track(object):
	def __init__(self, center, inner, outer):
		self.center = center
		self.inner = inner
		self.outer = outer

	def plot(self,ax):
		center, = ax.plot(self.center[:,0],self.center[:,1],'--',color='k')
		inner, = ax.plot(self.inner[:,0],self.inner[:,1],color='k')
		outer, = ax.plot(self.outer[:,0],self.outer[:,1],color='k')
		#return center, inner, outer

	def proximity(self,point):
		dist, idx = spatial.KDTree(self.center).query(point)
		return dist, self.center[idx]

def loadTrackData(trackFileName:str):
	data = np.load("./tracks/" + trackFileName)
	center = data[:,0:2]
	inner  = data[:,2:4]
	outer  = data[:,4:6]
	return center,inner,outer

def main():

	fig = plt.figure()
	ax = plt.subplot()

	center, inner, outer = loadTrackData('1.npy')
	track = Track(center, inner, outer)

	pt = [10,8.5]
	d, closept = track.proximity(pt)

	print(d)

	# Plot
	c,i,o = track.plot(ax)
	plt.plot([pt[0],closept[0]],[pt[1],closept[1]])


	ax.set_aspect('equal')
	ax.grid()
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
