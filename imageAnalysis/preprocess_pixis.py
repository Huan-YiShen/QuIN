import numpy as np
import matplotlib.pyplot as plt
from curvature_analysis import *
from curveFitting import *

def findThres(curvatureArea, intensityThreshold):
    # min = -2360 max = 4579 range = 6939
    bucket = np.arange(-24, 47)
    lowCount = 0
    highCount = 0
    for row in curvatureArea:
        for entry in row:
            if (entry<intensityThreshold):lowCount += 1
            else: highCount += 1
    print("lowCount = ", lowCount, "highCount = ", highCount)


def process(img):
    # gaussian blur
    kernel = generate_gaussian_filer(sigma = 0.6, filter_size = 10)
    curvatureArea_blurred = gaussian_blur(img, kernel)
    mpl_regenerateGrayImg(curvatureArea_blurred, "curvatureArea_blurred")

    # # bucket - bug 
    # mpl_regenerateGrayImg(bucketFilter(curvatureArea), "curvatureArea_bucket")

    binary_threshold = 160
    findThres(img, binary_threshold)
    curvatureArea_thres = np.where(curvatureArea_blurred < binary_threshold, 0, 255)
    mpl_regenerateGrayImg(curvatureArea_thres, "curvatureArea_blurred_thres0")

    # for i in range(170, 250, 10):
    #     print(i)
    #     findThres(curvatureArea, i)
    #     curvatureArea_thres = np.where(curvatureArea_blurred < i, 0, 255)
    #     mpl_regenerateGrayImg(curvatureArea_thres, "curvatureArea_blurred_thres_"+str(i))

    # intensity_matrix_thres = np.where(intensity_matrix < binary_threshold, 0, 255)
    # mpl_regenerateGrayImg_mpl(intensity_matrix_thres, "intensity_matrix_thres")


def findClosestData(value, dataSet):
    index = 0
    for ind, val in enumerate(dataSet):
        if (val <= value):
            continue
        else:
            index = ind
            break

    return index


def getCurvatureSample():
    # get data into np narray
    # old data
    # path = r".\labData\2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    # new data
    path = r"C:\Users\James\Documents\UWaterloo\3B_fall2023\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"
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
    waveLengthData = get_csv_wavelength(path)
    index_low = findClosestData(1170, waveLengthData)
    index_high = findClosestData(1300, waveLengthData)
    crop_x1 = 0
    crop_x2 = hor_len
    crop_y1 = 150
    crop_y2 = 400

    mask = np.ix_(np.arange(crop_y1, crop_y2), np.arange(crop_x1, crop_x2))
    # transport data 
    i_curvatureArea = intensity_matrix[mask].T
    mpl_regenerateGrayImg(i_curvatureArea, "curvatureArea_beforeProcessing")

    # generate threshold
    rangeMin = np.min(i_curvatureArea)
    rangeMax = np.max(i_curvatureArea)
    print("min = ", rangeMin, "max = ", rangeMax, "range = ", rangeMax-rangeMin)
    upperBound, lowerBound = filter_value_bounds(i_curvatureArea) 
    print("lowerThres = {:0.2f} UppwerThres = {:0.2f} Range = {:0.2f}".format(lowerBound, upperBound, upperBound-lowerBound))

    c = plt.imshow(i_curvatureArea, cmap ='gray', 
                   origin='lower', vmin = lowerBound, vmax = upperBound) 
    plt.colorbar(c) 
    
    return i_curvatureArea


'''

########## [ver_len, hor_len]
#                  #
#                  #
#                  #
#                  #
#                  #
#                  #
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

def findCurve(data):
    valid_curves = []
    # find a threashold 
    thres = 1000

    ver_len, hor_len = data.shape
    print(ver_len, hor_len)

    y_lim = 3315

    a = -0.15
    cx = int(hor_len/2)
    cy_range = np.arange(0, ver_len, 1)

    for cy in cy_range:
        a = -0.15
        # prepare parabola
        x, y = generate_probola(a, cx, cy, x_half_range=cx, y_lim=y_lim)
        # check if the curve fits
        doPlot = 0
        validPixelCount = verifyCurve(data, x, y, thres)
        print("verify {} {} {:0.2f}".format(cx, cy, validPixelCount/hor_len))
        if (validPixelCount > 0.9*hor_len): 
            doPlot = 1
        elif (validPixelCount > 0.7*hor_len): 
            # if we hit 60%, change the a value to see if we can do better
            stretchRange = np.arange(-1, 0, 0.005)        
            for stretch in stretchRange:
                x, y = generate_probola(stretch, cx, cy, x_half_range=cx, y_lim=y_lim)
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
         
    plt.ylim(0, ver_len)
    desnPath = "./output_curvature/" + "final" + ".png"
    plt.savefig(desnPath)
    plt.show()
    print(valid_curves)


if __name__ == '__main__':
    val = getCurvatureSample()
    findCurve(val)
    # store_as_csv("curvatureArea_transposed", val)
    print("Finished")
