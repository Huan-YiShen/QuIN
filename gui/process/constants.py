import numpy as np

###--- Constant
e = 1.60218E-19 # [C]
h = 4.13567E-15 # [eV*sec]
h_bar = 6.58212E-16 #[eV*sec]
c = 3.00E+08 # [m/sec]
me = 9.11E-31 # [kg]


###--- Function
def lorentzian(x, x0, A, FWHM):
    return (A / np.pi) * (FWHM / 2) / ((x - x0) ** 2 + (FWHM / 2) ** 2)

def gaussian(x, x0, A, sigma):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))
