import numpy as np
from process.constants import h_bar, e, me

class Result():
    def __init__(self, slope_um):
        self.slope_um = slope_um
        self.slope_m = slope_um * 1e-12 #[eV*m^2] = [eV^2*sec^2/kg]
        self.m_eff = h_bar**2/(self.slope_m)*e # CNT exciton effective mass?
        self.m_eff_rel = (self.m_eff)/me

    def print_result(self):
        print("slope_um = ", self.slope_um)
        print("slope_m = ", self.slope_m)
        print("m_eff = ", self.m_eff)
        print("m_eff_rel = ", self.m_eff_rel)


class AnalysisFigures():
    init_fig = None # initial figure
    cropped_fig = None # fine turned for parabola fits
    pixel_ev = None # pixel vs. ev with cropped parabola
    angle_ev = None # angle vs. ev with cropped parabola 
    kpara_ev = None # k-parallel vs. ev with cropped parabola


class ParabolaData():
    # data extracted from the 2D image directly
    base_x = np.array([]) # pixel index 
    base_y = np.array([]) # max eV for that pixel
    
    # x = pixel index of the parabola domain, base_x cropped
    # y = parabola fix for max eV over parabola domain
    parabola_x = np.array([]) # cropped_x
    parabola_y = np.array([]) # cropped eV

    # base_y vs. base_angles
    # parabola_y vs. parabola_angles
    base_angles = np.array([])
    parabola_angles = np.array([])

    # base_y vs. base_kpara
    # parabola_y vs. parabola_kpara
    base_kpara = np.array([])
    parabola_kpara = np.array([])

    # result class
    res = None