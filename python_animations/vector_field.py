#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import *

from matplotlib.animation import FuncAnimation
from PIL import Image

# setting path
sys.path.append('../library')
 
from eqdiff_solver import *

def eq_diff(x,y,a,b):
    u = x * (3 - a * x - b * y)
    v = y * (2 - x - y)
    return (u,v)

def update_plot(a=2, b=1, size=0.1):
    # Generate some random data
    x, y = np.meshgrid(np.arange(0, 3, size), np.arange(0, 3, size))
    u, v = eq_diff(x,y,a,b)

    # Calculate the magnitude of each vector and clip it so that we can get better coloring
    mag = np.clip(np.sqrt(u**2 + v**2), -10, 2)

    # Normalize the vectors
    norm = np.sqrt(u**2 + v**2)
    u = np.divide(u, norm, out=np.zeros_like(u), where=norm!=0)
    v = np.divide(v, norm, out=np.zeros_like(v), where=norm!=0)

    # Create the plot
    fig, ax = plt.subplots()

    # Set the colormap to 'cool'
    q = ax.quiver(x, y, u, v, mag, cmap='viridis')

    # Set the colorbar limits to the range of the magnitudes
    q.set_clim([mag.min(), mag.max()])

    # Set the colorbar ticks and labels
    cbar = plt.colorbar(q)
    cbar.set_ticks([mag.min(),(mag.min() + mag.max())/ 2, mag.max()])
    cbar.set_ticklabels(['Low', 'Medium', 'High'])
    
    plt.show()

update_plot()
