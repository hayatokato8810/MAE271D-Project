#!/usr/bin/env python

""" Numberline.py """

__author__ = "Hayato Kato"

import os
import sys
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir)

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class FourWheelCar():
	def __init__(self, trackData):
		print("Initializing")
		self.v = 0			# speed
		self.ax = 0			# longitudinal acceleration
		self.ay = 0			# lateral acceleration
		self.dn = 0			# normal distance to centerline
		self.alpha = 0	# angle relative to centerline
		self.slip = 0		# slip angle
		self.yaw = 0		# yaw rate

		self.track = trackData
		self.closestTrack = self.track[0]

		self.fig, self.axs = plt.subplots(1, 1, figsize=(9, 9))

	def plot(self):
		print("Plotting")
		self.plotTrack()
		plt.scatter(self.closestTrack[0],self.closestTrack[1],50,
			c='r',edgecolor='k', zorder=3)
		self.axs.set_xlim([-1,6])
		self.axs.set_ylim([-1,6])
		plt.grid(True)
		plt.show()

	def plotTrack(self):
		[tx,ty] = zip(*self.track)
		tx = tx + (self.track[0][0],)
		ty = ty + (self.track[0][1],)
		plt.plot(tx,ty,'-',color='grey',lw = 72,solid_capstyle='round', zorder=1)
		plt.plot(tx,ty,'--',color='white',lw = 2,solid_capstyle='round', zorder=2)

def main(args):
	print("Starting Program...")

	df = pd.read_csv('track data/' + args.input, delimiter=',')
	data = [tuple(row) for row in df.values]

	car = FourWheelCar(data)
	car.plot()

	print('Finishing Program...')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='RC Car Python Simulation')
	parser.add_argument('-i', '--input', help='CSV file name of track centerline coordinates', required=True)
	parser.add_argument('-o', '--output', help='Output data file name', required=False)
	args = parser.parse_args()
	main(args)