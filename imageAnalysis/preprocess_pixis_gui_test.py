import numpy as np
import matplotlib.pyplot as plt
from curvature_analysis import *
from curveFitting import *

def findClosestData(value, dataSet) -> int:
    index = 0
    wavelength = 0
    for ind, val in enumerate(dataSet):
        if (val <= value):
            continue
        else:
            index = ind
            break

    return index


def getCurvatureSample(path):
    # get data into np narray
    # old data
    # path = r".\labData\2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    # new data
    # path = r"C:\Users\James\Documents\UWaterloo\3B_fall2023\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"
    # path = r".\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-58_C-wave_575nm_40mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"
    intensity_matrix = np.array(get_csv_data(path))
    ver_len, hor_len = intensity_matrix.shape
    print("ver_len: ", ver_len, " | hor_len:", hor_len)

    # crop the image to where curvature should have been 11800, 12400
    ####### old data ########
    # crop_x1 = 11500
    # crop_x2 = 12800
    # crop_y1 = 150
    # crop_y2 = 350

    ######## new data ########
    #F57 - 1200~1300 wavelength
    #F58 - 1163~1300 wavelength
    cropWL1 = 1200
    cropWL2 = 1300
    waveLengthData = get_csv_wavelength(path)
    x_index_low = findClosestData(cropWL1, waveLengthData)
    x_index_high = findClosestData(cropWL2, waveLengthData)
    print("index_low = {}, index_high = {}".format(x_index_low, x_index_high))
    print(type(x_index_low))
    crop_x1 = x_index_low
    crop_x2 = x_index_high
    crop_y1 = 150
    crop_y2 = 400
    waveLengthData_cropped = waveLengthData[x_index_low : x_index_high]

    mask = np.ix_(np.arange(crop_y1, crop_y2), np.arange(crop_x1, crop_x2))
    # transport data 
    i_curvatureArea = intensity_matrix[mask].T

    return i_curvatureArea, waveLengthData_cropped


'''

########## [ver_len, hor_len]
#                  #
#                  #
#                  #
#                  #
##                ##
##                ##
##                ##
##                ##
# #              # #
# #              # #
#  #            #  #
#  #            #  #
#   #          #   #
#    #        #    #
#     #      #     #
#      ######      #
[0,0]############### 
'''

# def intenseRange(data, col, row, surrounding=1):
#     centerVal = data[col][row]
#     # include the surroundings
#     centerVal += data[col-1][row]
#     centerVal += data[col-1][row]

def verifyCurve(data:np.ndarray, x:int, y:int, thres:int):
    validPixelCount = 0
    for ind, col in enumerate(x):
        row = y[ind]
        if (data[row][col] > thres):
            validPixelCount += 1
    return validPixelCount


def findCurve(modifiedAxe, data):
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
        # print("verify {} {} {:0.2f}".format(cx, cy, validPixelCount/hor_len))
        if (validPixelCount > 0.9*hor_len): 
            doPlot = 1
        elif (validPixelCount > 0.7*hor_len): 
            # if we hit 60%, change the a value to see if we can do better
            for stretch in stretchRange:    # using a fixed stretchRange for now
                x, y = generate_parabola(stretch, cx, cy, x_half_range=cx, y_lim=y_lim)
                validPixelCount = verifyCurve(data, x, y, thres)
                # print("verify after 0.7 {} {} {:0.2f} {:0.2f}".format(cx, cy, validPixelCount/hor_len, stretch))
                if (validPixelCount > 0.9*hor_len): 
                    a = stretch
                    doPlot = 1
                    break

        if (doPlot):
            valid_curves.append((a, cy, cx))
            print("valid_curve: y_center", cy)
            modifiedAxe.plot(x, y)
            # plt.pause(0.005)
         
    modifiedAxe.set_ylim(0, ver_len)


def plot_rawData(img, wl : np.array):
    # produce plot
    mpl_regenerateGrayImg(img, "noCurve")

    # figure
    fig = plt.figure()
    pltNew = fig.add_subplot(111)
    pltNew.set_title("curvature Detection")
    pltNew.set_xlabel("pixels")
    pltNew.set_ylabel("wavelength [nm]")

    upperBound, lowerBound = filter_value_bounds(img) 
    c = pltNew.imshow(img, cmap ='gray', 
                   origin='lower', vmin = upperBound, vmax = lowerBound) 
    fig.colorbar(c, label = "intensity") 

    # get axies
    print("WL:", wl)
    r, c = img.shape
    interval = 500 
    wl_intervaled = [round(v, 2) for v in wl][0::interval]
    pltNew.set_yticks(np.arange(0, r, interval))
    pltNew.set_yticklabels(wl_intervaled)

    # figure = plt.gcf()
    # figure.set_figwidth(15)
    return fig


if __name__ == '__main__':
    path = r"C:\Users\James\Documents\UWaterloo\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"
    img, wavelength_axis = getCurvatureSample(path)
    rawFigure = plot_rawData(img, wavelength_axis)
    detectedFigure = plot_rawData(img, wavelength_axis)
    findCurve(detectedFigure.get_axes()[0], img)
    desnPath = "./output_curvature/" + "final" + ".png"
    detectedFigure.savefig(desnPath)
    detectedFigure.show()


    # store_as_csv("curvatureArea_transposed", val)
    print("Finished")
