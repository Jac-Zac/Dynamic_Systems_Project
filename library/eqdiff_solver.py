from numba import njit, float64, int32, vectorize, guvectorize
import matplotlib.pyplot as plt
from typing import Callable
import numpy as np
import time

## In all the following function we will use just in time compilation to speed up the computation easily around 20x


# Decorato to evaluate the speed of the function
def timer(func):
    "Timer decorator"

    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Executed {func.__name__!r} in {(end_time - start_time):.6f} seconds")
        return result

    return wrapper


@timer
@njit(cache=True)
def eulero(f, x0, dt=0.001, final_time=1) -> np.ndarray[float64]:
    """Differential equations solver using Euler's method"""
    # Initialize the solution array
    num_iterations = int32(final_time / dt)
    x = np.empty((num_iterations, x0.shape[0]))
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        x[i] = x[i - 1] + f(x[i - 1]) * dt

    # Return the final value of x
    return x


@timer
@njit(cache=True)
def eulero_modified(f, x0, dt=0.001, final_time=1) -> np.ndarray[float64]:
    """Differential equations solver using modified Euler's method"""
    # Initialize the solution array
    num_iterations = int32(final_time / dt)
    x = np.empty((num_iterations, x0.shape[0]))
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        x_hat = x[i - 1] + f(x[i - 1]) * dt
        x[i] = x[i - 1] + dt * (f(x[i - 1]) + f(x_hat)) / 2.0

    # Return the final value of x
    return x


@timer
@njit(cache=True)
def runge_kutta(f, x0, dt=0.001, final_time=1) -> np.ndarray[float64]:
    """Differential equations solver using Euler's method"""

    # Initialize the solution array
    num_iterations = int32(final_time / dt)
    x = np.empty((num_iterations, x0.shape[0]))
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        k1 = f(x[i - 1]) * dt
        k2 = f(x[i - 1] + k1 / 2.0) * dt
        k3 = f(x[i - 1] + k2 / 2.0) * dt
        k4 = f(x[i - 1] + k3) * dt
        x[i] = x[i - 1] + (1 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    # Return the final value of x
    return x


@njit(cache=True)
def vectorized_runge_kutta(f, x0_array, dt=0.001, final_time=1) -> np.ndarray:
    """Differential equations solver using Runge-Kutta method"""

    # Initialize the solution array
    num_iterations = int32(final_time / dt)
    num_conditions = x0_array.shape[0]
    x = np.empty((num_conditions, num_iterations, x0_array.shape[1]))
    x[:, 0] = x0_array

    for i in range(1, num_iterations):
        for j in range(num_conditions):
            k1 = f(x[j, i - 1]) * dt
            k2 = f(x[j, i - 1] + k1 / 2.0) * dt
            k3 = f(x[j, i - 1] + k2 / 2.0) * dt
            k4 = f(x[j, i - 1] + k3) * dt
            x[j, i] = x[j, i - 1] + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    return x


# Function to plot the solutions
def plot_solution(
    f, x0=np.array([0.1, 0.1]), dt=0.001, final_time: float64 = 1, rk_only=True
):
    # Set up the plot
    fig, ax = plt.subplots()

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

    # Compute trajactory
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


def phase_diagram_trajectories(
    f,
    dt: float64 = 0.1,
    final_time: float64 = 1,
    num: int = 20,
    start: int = -4,
    end: int = 4,
):
    # Generate all combinations of starting positions using nested for loops
    x_starts = np.linspace(start, end, num)
    y_starts = np.linspace(start, end, num)
    combinations = [(x, y) for x in x_starts for y in y_starts]

    # Initialize an array to store the trajectories
    trajectories = []

    # Solve the differential equation for each combination of x and y in a vectorized way
    x0_array = np.array(combinations)
    trajectories = vectorized_runge_kutta(f, x0_array, dt, final_time)

    # Set up the plot
    fig, ax = plt.subplots()

    # Define the color map
    cmap = plt.get_cmap("viridis")

    # Plot the trajectories for each combination of x and y
    for i in range(len(combinations)):
        x_traj = trajectories[i][:, 0]
        y_traj = trajectories[i][:, 1]
        color = cmap(i / len(combinations))
        ax.plot(x_traj, y_traj, color=color, linewidth=0.5)

    # Add labels and title
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(start, end)
    ax.set_ylim(start, end)
    ax.set_title(f'Trajectories of the Differential Equation, dt = {dt}')

    # Set the background color to white
    fig.patch.set_facecolor("white")

    # Remove the top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add grid lines
    ax.grid(True, linestyle="--", color="gray", alpha=0.5)

    # Show the plot
    plt.show()
