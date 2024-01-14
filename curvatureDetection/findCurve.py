import numpy as np
import os
import matplotlib.pyplot as plt
from curvature_analysis_helper import *
from parabola import *

######################################
## global parameter ##################
######################################
WAVELENGTH_INFO = [] # row dhat indicate the wavelength of the spectrometer
DATA = [] # intensity value of a 2D array (transposed)

######################################
## preprocessing #####################
######################################
def findClosestData(value, dataSet = WAVELENGTH_INFO) -> int:
    index = 0
    for ind, val in enumerate(dataSet):
        if (val <= value):
            continue
        else:
            index = ind
            break

    return index

# DEMO
def manualCrop(waveLengthInfo : np.ndarray, intensity_matrix : np.ndarray) -> np.ndarray:
    # crop base on wavelength value
    cropWL1 = 1200
    cropWL2 = 1300
    x_index_low = findClosestData(cropWL1, waveLengthInfo)
    x_index_high = findClosestData(cropWL2, waveLengthInfo)
    print("index_low = {}, index_high = {}".format(x_index_low, x_index_high))
    print(type(x_index_low))
    waveLengthData_cropped = waveLengthInfo[x_index_low : x_index_high]

    # crop again base on pixel index
    crop_x1 = x_index_low
    crop_x2 = x_index_high
    crop_y1 = 150
    crop_y2 = 400
    mask = np.ix_(np.arange(crop_y1, crop_y2), np.arange(crop_x1, crop_x2))

    return intensity_matrix[mask]


def extractDataFromPixis(path):
    intensity_matrix = np.array(get_csv_data(path))
    ver_len, hor_len = intensity_matrix.shape
    print("ver_len: ", ver_len, " | hor_len:", hor_len)

    waveLengthInfo = get_csv_wavelength(path)

    # data = manualCrop(waveLengthInfo, intensity_matrix).T
    data = intensity_matrix.T

    return (waveLengthInfo, data)


def setupDir():
    try:  
        os.mkdir("./output_img")
    except OSError:
        pass  
    print("LOG: output will be stroed in ./output_img/") 

    try:  
        os.mkdir("./output_log")
    except OSError:
        pass  
    print("LOG: output log will be stored in ./output_log/") 

######################################
## curve detection ###################
######################################
def verifyCurve(data:np.ndarray, x:int, y:int, thres:int):
    validPixelCount = 0
    for ind, col in enumerate(x):
        row = y[ind]
        if (data[row][col] > thres):
            validPixelCount += 1
    return validPixelCount


def findCurve(data):
    valid_curves = []
    # TODO: determine a intensity threshold where a pixel is deemed "bright" 
    thres = 1000
    ver_len, hor_len = data.shape

    # TODO: determine how much of the y-axis the parabola should display
    # y_lim = 3315
    y_lim = 1300

    # TODO: determine the vertical stretch allowed
    a = -0.15
    cx = int(hor_len/2)
    cy_range = np.arange(0, ver_len, 1)

    # TODO: determine a range of verital stretch we want to explore
    stretchRange = np.arange(-1, 0, 0.005)

    for cy in cy_range:
        a = -0.15
        # prepare parabola
        x, y = generate_parabola(a, cx, cy, x_half_range=cx, y_lim=y_lim)
        # check if the curve fits
        doPlot = 0
        validPixelCount = verifyCurve(data, x, y, thres)
        print("verify {} {} {:0.2f}".format(cx, cy, validPixelCount/hor_len))
        if (validPixelCount > 0.9*hor_len): 
            doPlot = 1
        elif (validPixelCount > 0.7*hor_len): 
            # if we hit 60%, change the a value to see if we can do better
            for stretch in stretchRange:    # using a fixed stretchRange for now
                x, y = generate_parabola(stretch, cx, cy, x_half_range=cx, y_lim=y_lim)
                validPixelCount = verifyCurve(data, x, y, thres)
                print("verify after 0.7 {} {} {:0.2f} {:0.2f}".format(cx, cy, validPixelCount/hor_len, stretch))
                if (validPixelCount > 0.9*hor_len): 
                    a = stretch
                    doPlot = 1
                    break

        if (doPlot):
            valid_curves.append((a, cy, cx))
            print("valid_curve: y_center", cy)
            plt.plot(x, y)
            # plt.pause(0.005)
         
    plt.ylim(0, ver_len)
    desnPath = "./output_curvature/" + "final" + ".png"
    plt.savefig(desnPath)
    plt.show()
    print(valid_curves)

######################################
## MAIN ##############################
######################################
if __name__ == '__main__':
    path = r"C:\Users\James\Documents\UWaterloo\3B_fall2023\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"

    setupDir()
    # preprocessing
    w, d = extractDataFromPixis(path)
    WAVELENGTH_INFO = w
    DATA = d
    # plot_rawData(img, wavelength_axis)
    print(DATA)
    print(WAVELENGTH_INFO)
    # curve detection
    # findCurve(img)

    # store_as_csv("curvatureArea_transposed", val)
    print("Finished")
