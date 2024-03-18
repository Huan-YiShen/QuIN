import numpy as np
from scipy.optimize import curve_fit

from process.constants import h
from process.constants import c
from process.constants import lorentzian
from process.constants import square
from process.constants import to_wl_nm

### --- analysis
def curveFit(data, wl):
    max_index = []
    max_wl = []
    max_eV = []

    if len(wl) != len(data[0]):
        print("ERR length of wavelength and data entry in a row does not match, len(wl) = ", len(wl), "len(data[0]) = ", len(data[0]))
        return

    for ind, pixelVals in enumerate(data):
        x_range = wl
        y_range = pixelVals
        
        initial_guess = [(wl[0]+wl[-1])/2,1,1]
    
        popt1, pcov1 = curve_fit(lorentzian, x_range, y_range, p0=initial_guess)
        
        max_index.append(ind)
        max_wl.append(popt1[0])
        max_eV.append(h*c/(popt1[0]*1e-9))
        
        # print(popt1[0], '_', h*c/(popt1[0]*1e-9))
    return max_index, max_wl, max_eV


def find_parabola(cropped_index, cropped_eV):
    quad_a = 1
    quad_b = 145
    quad_c = 1

    initial_guess = [quad_a, quad_b, quad_c]
    popt, _ = curve_fit(square, cropped_index, cropped_eV, p0=initial_guess)
    print('center: ', popt[1], 'and' ,  round(popt[1],0), ' / center lambda: ', to_wl_nm(popt[2]))
    return popt