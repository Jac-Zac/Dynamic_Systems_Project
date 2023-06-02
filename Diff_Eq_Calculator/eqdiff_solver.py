from numba import njit, float64, int32
import numpy as np
import time
# from matplotlib import pyplot as plt


def timer(func):
    "Timer decorator"
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(
            f"Executed {func.__name__!r} in {(end_time - start_time):.6f} seconds")
        return result
    return wrapper

@timer
@njit(cache=True)
def eulero(f: float64(float64), x0: float64 = 0.0, dt: float64 = 0.0000001, final_time: float64 = 1) -> np.ndarray[float64]:
    """ Differential equations solver using Euler's method"""
    # Initialize the solution array
    num_iterations = int32(final_time/dt)
    x = np.empty(num_iterations)
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        x[i] = x[i-1] + f(x[i-1]) * dt

    # Return the final value of x
    return x

@timer
@njit(cache=True)
def eulero_modified(f: float64(float64), x0: float64 = 0.0, dt: float64 = 0.0000001, final_time: float64 = 1) -> np.ndarray[float64]:
    """ Differential equations solver using Euler's method"""
    # Initialize the solution array
    num_iterations = int32(final_time/dt)
    x = np.empty(num_iterations)
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        x_hat = x[i - 1] + f(x[i - 1]) * dt
        x[i] = x[i - 1] + dt * (f(x_hat) + f(x[i - 1]))/2.0

    # Return the final value of x
    return x

@timer
@njit(cache=True)
def runge_kutta(f: float64(float64), x0: float64 = 0.0, dt: float64 = 0.0000001, final_time: float64 = 1) -> np.ndarray[float64]:
    """ Differential equations solver using Euler's method"""
    # Initialize the solution array
    num_iterations = int32(final_time/dt)
    x = np.empty(num_iterations)
    x[0] = x0

    # Iterate over all the elements except the first one
    for i in range(1, num_iterations):
        k1 = f(x[i - 1]) * dt
        k2 = f(x[i - 1] + k1/2.0) * dt
        k3 = f(x[i - 1] + k2/2.0) * dt
        k4 = f(x[i - 1] + k3) * dt
        x[i] = x[i - 1] + k1/6.0 + 2.0*k2 + 2.0*k3 + k4
        x[i] = x[i - 1] + (1/6.0)*(k1 + 2.0*k2 + 2.0*k3 + k4)

    # Return the final value of x
    return x

def plot_solution(f: float64(float64), x0: float64 = 0.0, dt: float64 = 0.0000001, final_time: float64 = 1):
    import matplotlib.pyplot as plt

    # Solve the differential equation using all three methods
    x_euler = eulero(f, x0, dt, final_time)
    x_euler_modified = eulero_modified(f, x0, dt, final_time)
    x_runge_kutta = runge_kutta(f, x0, dt, final_time)

    print(x_euler[-1])
    print(x_euler_modified[-1])
    print(x_runge_kutta[-1])

    # Compute the averages of x over intervals of length avg_window
    x_euler_avgs = np.mean(x_euler.reshape(-1, 100), axis=1)
    x_euler_modified_avgs = np.mean(x_euler_modified.reshape(-1, 100), axis=1)
    x_runge_kutta_avgs = np.mean(x_runge_kutta.reshape(-1, 100), axis=1)

    # Create a time array for plotting
    t = np.linspace(x0, final_time, len(x_euler_avgs))

    # Set up the plot
    fig, ax = plt.subplots()
    ax.plot(t, x_euler_avgs, label='Euler')
    ax.plot(t, x_euler_modified_avgs, label='Euler Modified')
    ax.plot(t, x_runge_kutta_avgs, label='Runge-Kutta')

    # Add labels and legend
    ax.set_xlabel('Time')
    ax.set_ylabel('Value of x')
    ax.set_title('Differential Equation Solutions')
    ax.legend()

    # Set the background color to white
    fig.patch.set_facecolor('white')

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add grid lines
    ax.grid(True, linestyle='--', color='gray', alpha=0.5)

    # Show the plot
    plt.show()


def plot_solution_second_order(f: Callable[[float64, float64], Tuple[float64, float64]], x0: float64 = 0.0, y0: float64 = 0.0, dt: float64 = 0.1, final_time: float64 = 10.0):
    import matplotlib.pyplot as plt
    # Create a grid of points in the x-y plane
    x, y = np.meshgrid(np.arange(-10, 10, 0.5), np.arange(-10, 10, 0.5))

    # Compute the derivatives of x and y at each point in the grid
    u, v = np.zeros_like(x), np.zeros_like(y)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            u[i,j], v[i,j] = f(x[i,j], y[i,j])

    # Normalize the derivatives to get unit vectors
    norm = np.sqrt(u**2 + v**2)
    u = u / norm
    v = v / norm

    # Plot the direction field
    plt.quiver(x, y, u, v, color='r')

    # Set the background color to white
    plt.gca().patch.set_facecolor('white')

    # Add grid lines
    plt.grid(True, linestyle='--', color='gray', alpha=0.5)

    # Show the plot
    plt.show()
