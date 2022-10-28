#!/usr/bin/env python

""" Numberline.py """

__author__ = "Hayato Kato"

import os
import sys
dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir)

import argparse
import pandas as pd
import numpy as np

class FourWheelCar():
	def __init__(self):
		print("Initializing")

	def plot(self):
		print("Plotting")


def main(args):
	print("Starting Program...")

	df = pd.read_csv(args.input, delimiter=',')
	data = [tuple(row) for row in df.values]

	print(data)

	print('Finishing Program...')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='RC Car Python Simulation')
	parser.add_argument('-i', '--input', help='CSV file name of track centerline coordinates', required=True)
	parser.add_argument('-o', '--output', help='Output data file name', required=False)
	args = parser.parse_args()
	main(args)