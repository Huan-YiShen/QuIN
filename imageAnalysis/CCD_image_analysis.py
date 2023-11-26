from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import csv


from curvature_analysis import *
# #################################################################
# parameters ######################################################
# #################################################################
# row count = element number from 1 to 4
# col count = group number from -2 to 9
# data from https://en.wikipedia.org/wiki/1951_USAF_resolution_test_chart
lp_mm_array = [
    [0.250, 0.500, 1.00, 2.00, 4.00, 8.00, 16.00, 32.0, 64.0, 128.0, 256.0, 512.0],
    [0.281, 0.561, 1.12, 2.24, 4.49, 8.98, 17.96, 35.9, 71.8, 143.7, 287.4, 574.7],
    [0.315, 0.630, 1.26, 2.52, 5.04, 10.08, 20.16, 40.3, 80.6, 161.3, 322.5, 645.1],
    [0.354, 0.707, 1.41, 2.83, 5.66, 11.31, 22.63, 45.3, 90.5, 181.0, 362.0, 724.1],
    [0.397, 0.794, 1.59, 3.17, 6.35, 12.70, 25.40, 50.8, 101.6, 203.2, 406.4, 812.7],
    [0.445, 0.891, 1.78, 3.56, 7.13, 14.25, 28.51, 57.0, 114.0, 228.1, 456.1, 912.3]
]

ccdImagePath = r"labData/2023_09_29_Image Data_FW/CCD_USAF1951_Gr5-Ele1_H.png"

pixelSize = 1.67 # micrometer
binary_threshold = 100 # range rfom 0-255
row_count_threshold = 30 # used in stage 3

group_num = -1
element_num = 1
line_pair_per_mm = lp_mm_array[element_num-1][group_num+2]


######################################################
# helper function
######################################################

# regenerate image from gray pixel using matplotlib  
def regenerateGrayImg_mpl(arr, name):
        plt.figure()
        plt.imshow(arr, cmap = 'gray')
        desnPath = "./output_resolution/" + name + ".png"
        plt.savefig(desnPath)
        return desnPath


# manual crop image
def crop_manual(gray_array, processed_array, name = "", display = 0):
         # crop image 
    # (currently index value is gnerated by manually inspecting processedARR_mpl)
    # (x1, y1) indicate top left, (x2, y2) indicate bottom right edge
    print("Instruction:")
    if (name == ""):
        print("please see blackwhite png in output_resolution/ directory")
    else :
        print(f"please see output_resolution/{name}.png")
    print("and provide the cropping locations, x1, y1, x2, and y2")
    print("\t(x1, y1) ---------------------------")
    print("\t    |         .      .      .      |")
    print("\t    |         .      .      .      |")
    print("\t    |         .      .      .      |")
    print("\t    --------------------------- (x2, y2)")
    x1 = int(input("x1 = "))
    y1 = int(input("y1 = "))
    x2 = int(input("x2 = "))
    y2 = int(input("y2 = "))

    # debug mode
    y1 = 700
    x1 = 1400
    y2 = 2000
    x2 = 1800
    # debug mode

    print("LOG: cropping images from pixel (", x1, ",", y1, ")", "to pixel (", x2, ",", y2, ")")
    print("LOG: cropped section indicated in output_resolution\cropped.png")

    crop_img = np.array(processed_array[y1:y2, x1:x2], copy=True)

    #cropping display
    if (display):
        crop_img_display = np.array(gray_array, copy = True)
        crop_img_display[y1:y2, x1:x2] = crop_img
        regenerateGrayImg_mpl(crop_img_display, name+"_cropped")

    return crop_img


# count pixel
def count_pixel(crop_img):
    barWidthData = 0
    accu_pix_count = 0
    pix_count = 0
    print("LOG: Computing size of the rectangle")
    for row in crop_img:
        for col in row:
             if col == 255: pix_count += 1
        if pix_count > row_count_threshold:
            barWidthData += 1
            accu_pix_count += pix_count
        pix_count = 0

    print("LOG: Total", accu_pix_count, "pixels detected in the cropped section")
    aveWidth = (accu_pix_count/barWidthData)/1000 # unit in mm
    aveHeight = (accu_pix_count/aveWidth)/1000 # unit in mm
    return aveWidth, aveHeight


# magnification process
def magnification_verif(aveWidth):
    physical_width = (1/line_pair_per_mm)/2
    print(line_pair_per_mm, " ", physical_width, " ", physical_width/aveWidth)
    return round(physical_width/aveWidth)


######################################################
# # numpy pixel array approach
######################################################
def manual_process(gray_array, name):
    # image processing
    processed_array = np.where(gray_array < binary_threshold, 0, 255)
    regenerateGrayImg_mpl(processed_array, name+"_thres"+str(binary_threshold))
    crop_img = crop_manual(gray_array, processed_array, name, 1)
    # count pixels
    aveWidth, aveHeight = count_pixel(crop_img)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("green bar Height is", aveHeight, "mm")
    print("green bar Width is", aveWidth, "mm")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    mag = magnification_verif(aveWidth)
    print("magnification:", mag)


def numpy_approach():
    # parameters
    try:  
        os.mkdir("./output_resolution") 
    except OSError:
        pass  
    print("LOG: output will be stroed in ./output_resolution/") 
    
    # ############################################### Stage 1
    # pixel generation from images 
    gray_array = np.array(Image.open(ccdImagePath).convert('L'))
    # image processing
    processed_array = np.where(gray_array < binary_threshold, 0, 255)
    regenerateGrayImg_mpl(processed_array, "processedARR_mpl")

    # ############################################### Stage 2
    crop_img = crop_manual(gray_array, processed_array, 1)
    # ############################################### Stage 3
    # count pixels
    aveWidth, aveHeight = count_pixel(crop_img)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("green bar Height is", aveHeight, "mm")
    print("green bar Width is", aveWidth, "mm")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    mag = magnification_verif(aveWidth)
    print("magnification:", mag)


    sp_path = r"labData/2023_09_29_Image Data_FW/"
    sp_file = r"SP_USAF1951_Gr5-Ele1_H.csv"
    sp_file_path = sp_path + sp_file
    sp_data = np.array(get_csv_data(sp_file_path))
    regenerateGrayImg_mpl(sp_data, sp_file)
    manual_process(sp_data, sp_file[:-4])
    


def generateSpImage(filePath):
    csv_path = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file)    
        for row in reader:
            csv_path.append(row[0])

    croppedDataList = []
    for path in csv_path:
        pathArr = path.split("\\")
        sp_data = np.array(get_csv_data(path))
        crop_data = np.array(sp_data[:, 900:1150], copy=True)
        regenerateGrayImg_mpl(crop_data, pathArr[-1][:-4])
        croppedDataList.append(crop_data)

    return croppedDataList


def processSpImages(croppedDataList):
    # for data in croppedDataList:
    data = croppedDataList[0]
    scaled_data = (data - np.min(data))/(np.max(data) - np.min(data))*255
    print(scaled_data)
    processed_array = np.where(scaled_data < 70, 0, 255)
    kernel = generate_gaussian_filer(20, 5)
    processed_matrix = gaussian_blur(processed_array, kernel)
    regenerateGrayImg_mpl(processed_matrix, "test")


if __name__ == "__main__":
    # parameters
    try:  
        os.mkdir("./output_resolution") 
    except OSError:
        pass  
    print("LOG: output will be stroed in ./output_resolution/") 
    # numpy_approach()
    croppedDataList = generateSpImage("data.csv")
    processSpImages(croppedDataList)
