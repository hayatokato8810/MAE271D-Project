import numpy as np

class Params:
	def __init__(self):
		self.N = 4  # Number of State Variables
		self.M = 1  # Number of Control Variables
		self.T = 10 # Prediction Horizon
		self.DT = 0.01 # Discretization Step

		self.MAX_STEER = 5