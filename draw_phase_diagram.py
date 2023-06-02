#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# define the sigmoid function
def sigmoid(x):
   return 1/(1+np.exp(-x))

a = 1
b = 2

# Generate some random data
x, y = np.meshgrid(np.arange(0, 3, 0.1), np.arange(0, 3, 0.1))
u = x * (3 - a * x - b * y)
v = y * (2 - x - y)

# Calculate the magnitude of each vector
mag = np.clip(np.sqrt(u**2 + v**2), -1,1)

# Create the plot
fig, ax = plt.subplots()

# Set the colormap to 'cool'
q = ax.quiver(x, y, u/(mag*20), v/(mag*20), mag, cmap='copper', scale_units='xy', scale=1)

plt.colorbar(q)
plt.show()
