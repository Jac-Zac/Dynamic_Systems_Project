#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from moviepy.editor import *
from PIL import Image

# setting path
sys.path.append("../library")
from eqdiff_solver import *


def eq_diff(x, y, a, b):
    u = x * (3 - a * x - b * y)
    v = y * (2 - x - y)
    return (u, v)


def update_plot(frame, a_min=1, a_max=3, b_min=1, b_max=3, size=0.1):
    # Calculate the values of a and b for this frame
    a = a_min + (a_max - a_min) * frame / frames
    b = b_min + (b_max - b_min) * frame / frames

    # Generate some random data
    x, y = np.meshgrid(np.arange(0, 3, size), np.arange(0, 3, size))
    u, v = eq_diff(x, y, a, b)

    # Calculate the magnitude of each vector and clip it so that we can get better coloring
    mag = np.clip(np.sqrt(u**2 + v**2), -10, 2)

    # Normalize the vectors
    norm = np.sqrt(u**2 + v**2)
    u = np.divide(u, norm, out=np.zeros_like(u), where=norm != 0)
    v = np.divide(v, norm, out=np.zeros_like(v), where=norm != 0)

    # Update the quiver plot
    q.set_UVC(u, v, mag)

    # Update the text objects
    text_a.set_position((0.95, 0.95))
    text_a.set_text(f"a = {a:.2f}")
    text_b.set_position((0.95, 0.875))
    text_b.set_text(f"b = {b:.2f}")

    return q, text_a, text_b


# Create the initial plot
fig, ax = plt.subplots()
x, y = np.meshgrid(np.arange(0, 3, 0.1), np.arange(0, 3, 0.1))
u, v = eq_diff(x, y, 2, 1)
mag = np.clip(np.sqrt(u**2 + v**2), -10, 2)
q = ax.quiver(x, y, u, v, mag, cmap="viridis")

# Add text objects for a and b
text_a = ax.text(
    0.95,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=11,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
)
text_b = ax.text(
    0.95,
    0.875,
    "",
    transform=ax.transAxes,
    fontsize=11,
    verticalalignment="top",
    horizontalalignment="right",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
)

# Add a title to the plot
ax.set_title("Quiver Plot of Differential Equation")

# Set the number of frames
frames = 24

# Create the animation
ani = FuncAnimation(
    fig, update_plot, frames=frames, fargs=(1, 3, 1, 3, 0.1), interval=100, repeat=True
)
ani1 = FuncAnimation(
    fig, update_plot, frames=frames, fargs=(1, 1, 1, 3, 0.1), interval=100, repeat=True
)
ani2 = FuncAnimation(
    fig, update_plot, frames=frames, fargs=(1, 3, 1, 1, 0.1), interval=100, repeat=True
)

# Save the animation as a GIF using PillowWriter
ani.save("gif1.gif", writer="pillow", fps=12)
ani1.save("gif2.gif", writer="pillow", fps=12)
ani2.save("gif3.gif", writer="pillow", fps=12)

# Create the 3 clips
clip1 = VideoFileClip("gif1.gif")
clip2 = VideoFileClip("gif2.gif")
clip3 = VideoFileClip("gif3.gif")

final_clip = concatenate_videoclips([clip1, clip2, clip3])
final_clip.write_gif("combined_animation.gif", fps=12)

plt.show()
plt.close("all")

# Create png for latex
# magick convert -coalesce combined_animation.gif combined_animation.png
