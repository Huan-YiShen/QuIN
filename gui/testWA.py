from process.processCSV import *
from process.curvatureDetection import *
from frame.WindowAnalysis import *
from process.generatePlot import bound_intensity_value
from process.generatePlot import findClosestData

def get_data_fit_curve():
    ## get data
    path = r'../data/FP-15_2024_02_29_FW_FP-15_C-wave_575nm_10.0mW_900-1400nm_Slit100_Center100_Trans_OL F-lens_1sec_SPF750LPFt800_f2-100_FW.csv'
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


def get_cropped_data():
    ## get data
    path = r'../data/FP-15_2024_02_29_FW_FP-15_C-wave_575nm_10.0mW_900-1400nm_Slit100_Center100_Trans_OL F-lens_1sec_SPF750LPFt800_f2-100_FW.csv'
    data = get_csv_data(path)
    wl = get_csv_wavelength(path)

    ########################################
    # parameter
    ########################################
    wlMin = findClosestData(980, wl)
    wlMax = findClosestData(1140, wl)
    crop_wl = wl[wlMin : wlMax]
    crop_pixels_range = (150, 350)
    ## 200, 330
    crop_intensity_range = (0, 1000)
    ########################################

    mask = np.ix_(np.arange(crop_pixels_range[0], crop_pixels_range[1]), np.arange(wlMin, wlMax))
    crop_data = bound_intensity_value(np.array(data)[mask], crop_intensity_range)

    return crop_data, crop_wl, crop_pixels_range, crop_intensity_range



def TEST_windowAnalysis():
    crop_data, crop_wl, crop_pixels, crop_intensity = get_cropped_data()
    WindowAnalysis(crop_data, crop_wl, crop_pixels, crop_intensity)


TEST_windowAnalysis()

tk.mainloop()