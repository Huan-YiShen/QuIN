import numpy as np
import os
import matplotlib.pyplot as plt
from curvature_analysis_helper import *
from parabola import *


######################################
## preprocessing #####################
######################################
def findClosestData(value, dataSet) -> int:
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
    waveLengthData_cropped = waveLengthInfo[x_index_low : x_index_high]

    # crop again base on pixel index
    crop_x1 = x_index_low
    crop_x2 = x_index_high
    crop_y1 = 150
    crop_y2 = 400
    mask = np.ix_(np.arange(crop_y1, crop_y2), np.arange(crop_x1, crop_x2))

    return intensity_matrix[mask], waveLengthData_cropped


def extractDataFromPixis(path, tb_logWindow = None):
    intensity_matrix = np.array(get_csv_data(path))
    ver_len, hor_len = intensity_matrix.shape
    print("ver_len: ", ver_len, " | hor_len:", hor_len)

    if (tb_logWindow is None):
        print("LOG extracting Data form file...\n")
    else:
        tb_logWindow.insert(END, "LOG extracting Data form file...\n")

    waveLengthInfo = get_csv_wavelength(path)

    intensity_matrix, waveLengthInfo = manualCrop(waveLengthInfo, intensity_matrix)
    intensity_matrix = intensity_matrix.T
    print("waveLengthInfo", len(waveLengthInfo))
    print("data", intensity_matrix.shape)
    return waveLengthInfo, intensity_matrix


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


def findCurve(data, wl):
    # create a base line figure
    fig = plt.figure(dpi = 100)
    resultPlt = fig.add_subplot(111)
    resultPlt.set_title("Curve Detected")
    resultPlt.set_xlabel("pixels")
    resultPlt.set_ylabel("wavelength [nm]")
    upperBound, lowerBound = filter_value_bounds(data) 
    c = resultPlt.imshow(data, cmap ='gray', 
                   origin='lower', vmin = upperBound, vmax = lowerBound) 
    fig.colorbar(c, label = "intensity")
    r, c = data.shape
    interval = 500 
    wl_intervaled = [round(v, 2) for v in wl][0::interval]
    resultPlt.set_yticks(np.arange(0, r, interval))
    resultPlt.set_yticklabels(wl_intervaled)


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
        # print("verify {} {} {:0.2f}".format(cx, cy, validPixelCount/hor_len)) # DEBUG
        if (validPixelCount > 0.9*hor_len): 
            doPlot = 1
        elif (validPixelCount > 0.7*hor_len): 
            # if we hit 60%, change the a value to see if we can do better
            for stretch in stretchRange:    # using a fixed stretchRange for now
                x, y = generate_parabola(stretch, cx, cy, x_half_range=cx, y_lim=y_lim)
                validPixelCount = verifyCurve(data, x, y, thres)
                # print("verify after 0.7 {} {} {:0.2f} {:0.2f}".format(cx, cy, validPixelCount/hor_len, stretch)) # DEBUG
                if (validPixelCount > 0.9*hor_len): 
                    a = stretch
                    doPlot = 1
                    break

        if (doPlot):
            valid_curves.append((a, cy, cx))
            # print("valid_curve: y_center", cy)  # DEBUG
            resultPlt.plot(x, y)
            # plt.pause(0.005)
         
    resultPlt.set_ylim(0, ver_len)
    desnPath = "./output_img/" + "final" + ".png"
    fig.savefig(desnPath)
    # plt.show()
    # print(valid_curves)

    return fig

######################################
## MAIN ##############################
######################################
if __name__ == '__main__':
    path = r"C:\Users\James\Documents\UWaterloo\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"

    setupDir()
    # preprocessing
    w, d = extractDataFromPixis(path)
    plot_rawData(d, w)
    # curve detection
    findCurve(d, w)

    # store_as_csv("curvatureArea_transposed", val)
    print("Finished")
