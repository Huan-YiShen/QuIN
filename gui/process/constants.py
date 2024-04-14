import numpy as np

###--- Constant
e = 1.60218E-19 # [C]
h = 4.13567E-15 # [eV*sec]
h_bar = 6.58212E-16 #[eV*sec]
c = 3.00E+08 # [m/sec]
me = 9.11E-31 # [kg]

lambda_ref = 1010*1e-9 # [m]
pixel_max = 115
pixel_min = -115

###--- Function
def lorentzian(x, x0, A, FWHM):
    return (A / np.pi) * (FWHM / 2) / ((x - x0) ** 2 + (FWHM / 2) ** 2)

def gaussian(x, x0, A, sigma):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))

def square(x, a, b, c):
    return a*(x - b)**2 + c

###--- helpers
def to_eV( wl : np.array.__class__):
    wl_meter = (wl)*1e-9
    return h*c/(wl_meter)


def to_wl_nm(eV : np.array.__class__):
    wl_nm = (eV)*1e9
    return h*c/wl_nm


###--- Linear relation: pixel to angle
def pixel2angle_linear(index_array, parabolaVertex):
    print("pixel2angle_linear(): ", parabolaVertex)
    print("index_array: ", index_array)

    theta_max = np.arcsin(0.85)*180/np.pi
    slope = theta_max / pixel_max

    max_index_shift = index_array - round(parabolaVertex, 0)
    return slope*max_index_shift


def angle2k_ll(angle_array):
    return 2*np.pi*np.sin(angle_array*np.pi/180)/lambda_ref
