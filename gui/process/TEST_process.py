from curvatureDetection import curveFit

from generatePlot import plot_curveFit

from processCSV import get_csv_data
from processCSV import get_csv_wavelength

import matplotlib.pyplot as plt


def test_curveFit():
    path = '../../data/FP-15_C-wave_575nm_10.0mW_900-1400nm_Slit100_Center100_Trans_OL F-lens_1sec_SPF750LPFt800_f2-100_FW.csv'

    data = get_csv_data(path)
    wl = get_csv_wavelength(path)


    max_index, max_wl, max_eV = curveFit(data, wl)
    fig = plot_curveFit(plt.figure(dpi = 100), max_index, max_eV)
    plt.show()

test_curveFit()