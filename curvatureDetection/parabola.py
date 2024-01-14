import numpy as np
import matplotlib.pyplot as plt
from curvature_analysis_helper import *

# x_half_range is the total x range/2 centered at xc
def generate_parabola(a, xc, yc, x_half_range = 10, y_lim = 9999999):
    x = np.arange(xc-x_half_range, xc+x_half_range, 1)
    # y = a*(x**2) + b*(x) + c  
    y = a*((x-xc)**2) + yc

    # filter result to be mapped to 2D array
    yr = [-y_lim if i < -y_lim else i for i in y]
    return x, (np.round(yr)).astype(int)

def plot_hori_stretch(ai = 1, bi = 1, ci = 1, increment = 1, ranges = 10):
    a = ai
    b = bi
    c = ci
    for _ in range(ranges):
        x, y = generate_parabola(a, b, c)
        plt.plot(x, y)
        a += increment

def plot_vertical_shift(ai = 1, bi = 1, ci = 1, increment = 1, ranges = 10):
    a = ai
    b = bi
    c = ci
    for _ in range(ranges):
        x, y = generate_parabola(a, b, c)
        plt.plot(x, y)
        c += increment

# plot_vertical_shift()
# # plot_hori_stretch()
# plt.show()
