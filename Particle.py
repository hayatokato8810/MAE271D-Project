import math

class Particle():
	def __init__(self, x, y, theta):
		self.x = x
		self.y = y
		self.theta = theta

	def update(self, r):
		
		x_dot = v_x * math.cos(self.theta) - v_y * math.sin(self.theta)
		pass

def main():
	print("Starting")

	#fig = plt.figure()
	#ax = plt.subplot()

	p = Particle(0,0,0)
	p.update(1)






if __name__ == '__main__':
	main()