import numpy as np
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import LinearRing, LineString
import pandas as pd
import matplotlib.pyplot as plt
import os.path

__author__ = "Varit Vichathorn"

# Ask user for which track number to use
print('Select the track number: ')
trackNumber = input('')

# Load the center, inner, outer waypoints
waypoints = np.load("./tracks/%s.npy" % trackNumber)
txi = waypoints[:,2]  #inner
tyi = waypoints[:,3]
inner_border = waypoints[:,2:4]

tx = waypoints[:,0]   #center
ty = waypoints[:,1]
center_line = waypoints[:,0:2]


txo = waypoints[:,4]  #outer
tyo = waypoints[:,5]
outer_border = waypoints[:,4:6]


l_center_line = LineString(center_line)
l_inner_border = LineString(inner_border)
l_outer_border = LineString(outer_border)



# Plot track
ax = plt.axes()
ax.set_facecolor("green")
plt.plot(tx,ty,'-',color='grey',lw =35,solid_capstyle='round', zorder=1)
center_line_plot = plt.plot(tx,ty,'--',color='white',solid_capstyle='round', zorder=1,label='Center line')
inner_line_plot = plt.plot(txi,tyi,'k', label="Track boundary",lw =2)
outer_line_plot = plt.plot(txo,tyo, 'k',lw =2)
plt.legend(loc="lower left")
plt.title("Track #%s" %trackNumber)
plt.show()
################################################################
