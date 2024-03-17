import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from processCSV import *

def lorentzian(x, x0, A, FWHM):
    return (A / np.pi) * (FWHM / 2) / ((x - x0) ** 2 + (FWHM / 2) ** 2)

def gaussian(x, x0, A, sigma):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))

def square(x, a, b, c):
    return a*(x - b)**2 + c


h = 4.13567E-15 # [eV*sec]
h_bar = 6.58212E-16 #[eV*sec]
c = 3.00E+08 # [m/sec]

############################################################################################
############################################################################################
############################################################################################

def to_eV( wl : np.array.__class__):
    wl_meter = (wl)*1e-9
    return h*c/(wl_meter)


def to_wl_nm(eV : np.array.__class__):
    wl_nm = (eV)*1e9
    return h*c/wl_nm


def find_parabola(cropped_index, cropped_eV):
    quad_a = 1
    quad_b = 145
    quad_c = 1

    initial_guess = [quad_a, quad_b, quad_c]
    popt, _ = curve_fit(square, cropped_index, cropped_eV, p0=initial_guess)
    print('center: ', popt[1], 'and' ,  round(popt[1],0), ' / center lambda: ', to_wl_nm(popt[2]))
    return popt


def plot_parabola_overlay(max_index, max_eV, popt):
    plt.plot(max_index, max_eV)
    plt.plot(max_index, square(max_index, popt[0],popt[1],popt[2]))
    plt.xlabel('Pixel')
    plt.ylabel('Energy (eV)')

############################################################################################
############################################################################################
############################################################################################


def get_data_fit_curve():
    ## get data
    path = r'../../data/FP-15_2024_02_29_FW_FP-15_C-wave_575nm_10.0mW_900-1400nm_Slit100_Center100_Trans_OL F-lens_1sec_SPF750LPFt800_f2-100_FW.csv'
    data = get_csv_data(path)
    wl = get_csv_wavelength(path)

    ## get 
    max_index = []
    max_wl = []
    max_eV = []

    if len(wl) != len(data[0]):
        print("ERR length of wavelength and data entry in a row does not match, len(wl) = ", len(wl), "len(data[0]) = ", len(data[0]))

    for ind, pixelVals in enumerate(data):
        x_range = wl
        y_range = pixelVals
        
        initial_guess = [(wl[0]+wl[-1])/2,1,1]

        popt1, pcov1 = curve_fit(lorentzian, x_range, y_range, p0=initial_guess)
        
        max_index.append(ind)
        max_wl.append(popt1[0])
        max_eV.append(h*c/(popt1[0]*1e-9))
        
        print(popt1[0], '_', h*c/(popt1[0]*1e-9))

    return max_index, max_wl, max_eV




max_index, max_wl, max_eV = get_data_fit_curve()

###--- Set fitting range
quad_ini = 180
quad_las = 320

fit_ylim_ini = 1.00
fit_ylim_las = 1.05
plt.ylim(fit_ylim_ini,fit_ylim_las)

cropped_index = max_index[quad_ini:quad_las]
cropped_eV = max_eV[quad_ini:quad_las]
plt.plot(cropped_index, cropped_eV)
plt.xlabel('Pixel')
plt.ylabel('Energy (eV)')

plt.show()


###--- find parabola
popt = find_parabola(cropped_index, cropped_eV)

###--- Fitting result check
plot_parabola_overlay(cropped_index, cropped_eV, popt)
# plt.ylim(fit_ylim_ini,fit_ylim_las)
plt.show()