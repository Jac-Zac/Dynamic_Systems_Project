#!/usr/bin/env python3

from eqdiff_solver import plot_solution
from numba import njit, float64
import math

@njit(cache=True)
def f(x: float64) -> float64:
    return 0.2 * x**2 - 3.0

def main():
    # Define the differential equation
    plot_solution(f,x0=1, dt=0.0001, final_time=100)

if __name__ == "__main__":
    main()

############# Future Work #############
