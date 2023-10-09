import numpy as np
import matplotlib.pyplot as plt
import csv
from PIL import Image

# read image as an 2D array 

def get_img(filePath):
    file_data = []
    gray_image = []
    skipHeaderRows = 4
    skipFooterRows = 4
    with open(filePath, 'r') as file:
        reader = csv.reader(file)    
        for row in reader:
            file_data.append(row[1:])

    while skipFooterRows > 0:
        del file_data[-1]
        skipFooterRows -= 1

    while skipHeaderRows > 0:
        file_data.pop(0)
        skipHeaderRows -= 1


    for row in file_data:
        gray_image.append(np.array(row, dtype = int))

    print("Finish parsing the images...")
    return gray_image


def process_relative_value(intensity_data : np.ndarray) -> np.ndarray:
    max_val = np.amax(intensity_data)
    min_val = np.amin(intensity_data)
    print("max_val = ", max_val, ", min_val = ", min_val)
    adjustment_ratio = 255/(max_val - min_val)
    # intensity_data = intensity_data + abs(min_val)
    return intensity_data
    # return (intensity_data*adjustment_ratio).round().astype(int)

def crop_images(gray_img):
    ver_len, hor_len = gray_img.shape
    # crop images
    gray_img_cropped_list = []

    hor_ind_start = 0
    hor_ind_end = ver_len
    hor_corp_len = ver_len
    crop_count = int(hor_len/hor_ind_end) + 1

    print("Crop image into", crop_count, "pieces...")
    cropped_img = []
    for _ in range(0, crop_count):
        # creating one cropped image
        for row in gray_img:
            cropped_img.append(row[hor_ind_start : hor_ind_end])
        
        gray_img_cropped_list.append(cropped_img)
        # reset for next cropped image
        cropped_img = []
        # slide the cropping window to the next images 
        hor_ind_start = hor_ind_end
        hor_ind_end += hor_corp_len
        # last image edge case
        if (hor_ind_end > hor_len): hor_ind_end = hor_len


    print("Finish cropping the images...")
    print("generating png of the cropped image...")
    # display the images
    for i, gray_img_cropped in enumerate(gray_img_cropped_list):
        plt.figure(figsize = (10, 5))
        plt.imshow(gray_img_cropped, cmap = 'gray')
        plt.title('Grayscale Image' + str(i))
        plt.savefig("output/cropped_" + str(i) + ".png")
        # plt.show()


def main(testFilePath):
    # [[1, 2, 3, 5], [1, 2, 3, 5]]
    intensity_matrix = np.array(get_img(testFilePath))
    ver_len, hor_len = intensity_matrix.shape
    print("vertical pixel count = ", ver_len, "horizontal pixel count = ", hor_len)

    gray_img = process_relative_value(intensity_matrix)
    print(gray_img)
    pil_img = Image.fromarray(gray_img, mode = "L")
    print(pil_img.mode)
    pil_img.save('gray_img.png')

    ## print(gray_img)
    ## plt.figure(figsize=(hor_len/100, ver_len/100))
    # plt.figure()
    # plt.imshow(gray_img, cmap = 'gray')
    # plt.title('Grayscale Image')
    # plt.savefig('grayscaleFull.svg', format = 'svg', dpi=1200)
    ## plt.show()
 

if __name__ == '__main__':
    testFilePath = "labData/2023_09_29_Image Data_FW\SP_USAF1951_Gr5-Ele1_H.csv"
    testFilePath = "labData/2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    main(testFilePath)
    print("DONEEEEEEE")
