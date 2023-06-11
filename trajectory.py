#!/usr/bin/env python3

from matplotlib.animation import FuncAnimation
from PIL import Image

from library.eqdiff_solver import *

from numba import njit
import numpy as np

# remeber that x can be multi dimensional so the function is general to n dimensino
@njit(cache=True)
def f(x) -> np.ndarray[float64]:

    # Define the value for a and b
    a = 2.0
    b = 1.0

    # Define the equations
    u = x[0] * (3 - a * x[0] - b * x[1])
    v = x[1] * (2 - x[0] - x[1])
    return np.array([u, v])


# Function to plot the solutions
def animated_showcase(f, x0=np.array([0.1, 0.1]), dt=0.001, final_time: float64 = 1, rk_only=True):
    # Set up the plot
    fig, ax = plt.subplots()

    def update(dt):
        ax.clear()

        # Solve the differential equation using all three methods
        if rk_only == False:
            # Compute trajectory
            x_euler = eulero(f, x0, dt, final_time)
            x_euler_modified = eulero_modified(f, x0, dt, final_time)

            # Extract the x and y coordinates of the trajectory
            x_traj_euler = x_euler[:, 0]
            y_traj_euler = x_euler[:, 1]
            x_traj_euler_modified = x_euler_modified[:, 0]
            y_traj_euler_modified = x_euler_modified[:, 1]

            # Plot the trajectory for each method
            ax.plot(x_traj_euler, y_traj_euler, label="Euler")
            ax.plot(x_traj_euler_modified, y_traj_euler_modified, label="Euler Modified")

        # Compute trajectory
        x_runge_kutta = runge_kutta(f, x0, dt, final_time)

        # Extract the x and y coordinates of the trajectory
        x_traj_runge_kutta = x_runge_kutta[:, 0]
        y_traj_runge_kutta = x_runge_kutta[:, 1]

        # Plot the trajectory for Runge-Kutta
        ax.plot(x_traj_runge_kutta, y_traj_runge_kutta, label="Runge-Kutta")

        # Add labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Trajectory of the Differential Equation Solution")

        # Set the background color to white
        fig.patch.set_facecolor("white")

        # Remove the top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Add grid lines
        ax.grid(True, linestyle="--", color="gray", alpha=0.5)

        # Add legend
        ax.legend()

        # Add text box with dt value
        ax.text(0.95, 0.05, "dt = {:.3f}".format(dt), transform=ax.transAxes, fontsize=10,
                verticalalignment='bottom', horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    # Create the animation
    dt_values = np.linspace(0.9, 0.001, 100)
    ani = FuncAnimation(fig, update, frames=dt_values, interval=100, repeat=True)

    # Save the animation as a GIF using PillowWriter
    ani.save("numerical_showcase.gif", writer="pillow", fps=12)

    # Show the plot
    plt.show()

animated_showcase(f=f)
