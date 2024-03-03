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


# get wavelegnth data and intensity data from csv file
# PARA  path -> str, tb_loWindow -> tk.Text
# RTN   waveLengthInfo -> list, intensity_matrix -> np.ndarray
def extractDataFromPixis(path, tb_logWindow = None):
    intensity_matrix = np.array(get_csv_data(path))
    ver_len, hor_len = intensity_matrix.shape
    print("ver_len: ", ver_len, " | hor_len:", hor_len)
    if (tb_logWindow is None):
        print("ERR tb_logWindow is None...\n")
    # else:
    #     tb_logWindow.insert(END, "DEBUG extracting Data form file...\n")

    waveLengthInfo = get_csv_wavelength(path)

    # for DEMO
    intensity_matrix, waveLengthInfo = manualCrop(waveLengthInfo, intensity_matrix) ############################## TODO: do it in GUI
    # for DEMO
    crop_x1 = 0
    crop_x2 = len(intensity_matrix[0])
    crop_y1 = 150
    crop_y2 = 400
    # mask = np.ix_(np.arange(crop_y1, crop_y2), np.arange(crop_x1, crop_x2))

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
        try: int_val = data[row][col]
        except: break
        if (int_val > thres):
            validPixelCount += 1

    return validPixelCount


def findCurve(fig, data, wl):
    # create a base line figure TODO: reuse plot_rawData()
    ###############################
    # fig = plt.figure(dpi = 100)
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

    ###############################
    ###### manual parameters ######
    ###############################
    valid_curves = []
    # TODO: determine a intensity threshold where a pixel is deemed "bright" 
    thres = 1000
    ver_len, hor_len = data.shape

    # TODO: determine how much of the y-axis the parabola should display
    # y_lim = 3315
    y_lim = 1300

    pixel_resolution = 10
    x_center = int(hor_len/2)
    x_range = 40
    cx_range = np.arange(x_center-x_range, x_center+x_range, pixel_resolution)
    cy_range = np.arange(0, ver_len, pixel_resolution)
    # TODO: determine a range of verital stretch we want to explore
    a = -0.15
    stretchRange = np.arange(-1, 0, 0.005)

    ###############################
    ########## detection ##########
    ###############################
    for cx in cx_range:
        print("x_center: ", cx)
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
    print(valid_curves)
    write_detection_result(valid_curves) 
    return fig

######################################
## MAIN ##############################
######################################
if __name__ == '__main__':
    path = r"C:\Users\James\Documents\UWaterloo\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"

    setupDir()
    # preprocessing
    w, d = extractDataFromPixis(path)
    fig = plt.figure(dpi = 100)
    plot_rawData(fig, d, w)
    # curve detection
    fig1 = plt.figure(dpi = 100)
    findCurve(fig1, d, w)
    plt.show()
    # store_as_csv("curvatureArea_transposed", val)
    print("Finished")
