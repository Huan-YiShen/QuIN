import numpy as np
from scipy.optimize import curve_fit


###--- Function

def lorentzian(x, x0, A, FWHM):
    return (A / np.pi) * (FWHM / 2) / ((x - x0) ** 2 + (FWHM / 2) ** 2)

def gaussian(x, x0, A, sigma):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))


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
    
        popt1, pcov1 = curve_fit(lorentzian, x1_range, y1_range, p0=initial_guess1)
        
        max_index.append(i)
        max_wl.append(popt1[0])
        max_eV.append(h*c/(popt1[0]*1e-9))
        
        print(popt1[0], '_', h*c/(popt1[0]*1e-9))


def plot_fit():
    plt.plot(max_index, max_eV)
    plt.xlabel('Pixel')
    plt.ylabel('Energy (eV)')


    fit_ylim_ini = 1.05
    fit_ylim_las = 1.2


    plt.ylim(fit_ylim_ini,fit_ylim_las)