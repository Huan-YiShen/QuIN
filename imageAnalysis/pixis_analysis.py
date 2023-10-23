import numpy as np
import matplotlib.pyplot as plt
import csv
from PIL import Image
from curvature import *

def get_csv_data(filePath):
    file_data = []
    matrix_data = []
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
        matrix_data.append(np.array(row, dtype = int))

    print("Finish retrieving data from csv...")
    return matrix_data

def main(testFilePath):
    # [[1, 2, 3, 5], [1, 2, 3, 5]]
    intensity_matrix = np.array(get_csv_data(testFilePath))
    ver_len, hor_len = intensity_matrix.shape
    print("vertical pixel count = ", ver_len, "horizontal pixel count = ", hor_len)

    # transpose the image 
    intensity_matrix = intensity_matrix.T

    kernel = generate_gaussian_filer(20, 3)
    processed_matrix = gaussian_blur(intensity_matrix, kernel)

    # print(gray_img)
    plt.figure(figsize=(hor_len/100, ver_len/100))
    plt.imshow(processed_matrix, cmap = 'gray')
    plt.title('Grayscale Image')
    plt.savefig("./output_curvature/matlab.png")

if __name__ == '__main__':
    # testFilePath = "labData/2023_09_29_Image Data_FW\SP_USAF1951_Gr5-Ele1_H.csv"
    testFilePath = "labData/2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    main(testFilePath)
    print("Finished")
