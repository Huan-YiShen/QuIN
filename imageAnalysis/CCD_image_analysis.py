from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os 

# parameters
ccdImagePath = r"labData/2023_09_29_Image Data_FW/CCD_USAF1951_Gr5-Ele1_H.png"
pixelSize = 1.67 # micrometer


######################################################
# helper function
######################################################
# regenerate image from gray pixel using python image library
def regenerateGrayImg(arr, name, csvGen = 0):
    # regenerate image
    pil_img = Image.fromarray(arr, 'L')
    pil_img.save("output_resolution/" + name + '.jpg')
    if (csvGen):
        np.savetxt("output_resolution/" + name + ".csv", arr, delimiter=",")


# regenerate image from gray pixel using matplotlib  
def regenerateGrayImg_mpl(arr, name):
        plt.figure()
        plt.imshow(arr, cmap = 'gray')
        plt.savefig("./output_resolution/" + name + ".png")

######################################################
#  numpy pixel array approach
######################################################
def numpy_approach():
    # parameters
    binaryThreshold = 100
    try:  
        os.mkdir("./output_resolution") 
    except OSError:
        pass  
    print("LOG: output will be stroed in ./output_resolution/") 
    
    # pixel generation from images 
    gray_array = np.array(Image.open(ccdImagePath).convert('L'))
    # image processing
    processed_array = np.where(gray_array < binaryThreshold, 0, 255)
    regenerateGrayImg_mpl(processed_array, "processedARR_mpl")

    # crop image 
    # (currently index value is gnerated by manually inspecting processedARR_mpl)
    # (x1, y1) indicate top left, (x2, y2) indicate bottom right edge
    print("Instruction:")
    print("please see output_resolution/processedARR_mpl.png")
    print("and provide the cropping locations, x1, y1, and y2")
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
    crop_img_display = np.array(gray_array, copy = True)
    crop_img_display[y1:y2, x1:x2] = crop_img
    regenerateGrayImg_mpl(crop_img_display, "cropped")

    # count pixels
    barWidthData = 0
    accu_pix_count = 0
    pix_count = 0
    print("LOG: Computing size of the rectangle")
    pixel_counter = 0
    for row in crop_img:
        for col in row:
             if col == 255: pix_count += 1
        if pix_count > 30:
             barWidthData += 1
        accu_pix_count += pix_count
        pix_count = 0

    print("LOG: Total", accu_pix_count, "pixels detected in the cropped section")
    aveWidth = accu_pix_count/barWidthData 
    aveHeight = accu_pix_count/aveWidth

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("green bar Height is", aveHeight/1000, "mm")
    print("green bar Width is", aveWidth/1000, "mm")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
###################################################### 
# # CV2 approach
######################################################
def cv2_approach():
    # load the example image
    image = cv2.imread(ccdImagePath)
    image = cv2.resize(image, (0, 0), fx = 0.1, fy = 0.1)

    # pre-process the image by resizing it, converting it to
    # graycale, blurring it, and computing an edge map
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(edged, 255, 1, 1, 11, 1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    samples = np.empty((0, 100))
    responses = []

    window_name = 'image'
    cv2.imshow(window_name, thresh)
    key = cv2.waitKey(0)


if __name__ == "__main__":
     numpy_approach()