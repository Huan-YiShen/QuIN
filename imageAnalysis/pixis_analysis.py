import numpy as np
import matplotlib.pyplot as plt
import csv
from PIL import Image
from curvature import *

# regenerate image from gray pixel using python image library
def pil_regenerateGrayImg(arr, name, csvGen = 0):
    # regenerate image
    pil_img = Image.fromarray(arr, 'L')
    pil_img.save("output_curvature/" + name + '.jpg')
    if (csvGen):
        np.savetxt("output_curvature/" + name + ".csv", arr, delimiter=",")

def mpl_regenerateGrayImg(arr, name):
        plt.figure()
        plt.imshow(arr, cmap = 'gray')
        desnPath = "./output_curvature/" + name + ".png"
        plt.savefig(desnPath)
        return desnPath

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

    print(f"Finish retrieving data from csv {filePath}...")
    return matrix_data

def bucketFilter(curvatureArea):
    # min = -2360 max = 4579 range = 6939
    min = -23
    max = 47
    bucket = np.arange(min, max)
    # rangeVal = max-min
    # step = 255/rangeVal

    res = np.zeros(curvatureArea.shape, np.float32)
    for y, row in enumerate(curvatureArea):
        for x, entry in enumerate(row):
            for val in bucket:
                if (entry < val):
                    res[y][x] = int(entry/100) + 1
                    break 

    return res

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

def getCurvatureSample():
    path = r".\labData\2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    intensity_matrix = np.array(get_csv_data(path))
    ver_len, hor_len = intensity_matrix.shape
    print("ver_len: ", ver_len, " | hor_len:", hor_len)
    
    mask = np.ix_(np.arange(0, ver_len), np.arange(11800, 12400))
    curvatureArea = intensity_matrix[mask]
    mpl_regenerateGrayImg(curvatureArea, "curvatureArea_beforeProcessing")
    rangeMin = np.min(curvatureArea)
    rangeMax = np.max(curvatureArea)
    print("min = ", rangeMin, "max = ", rangeMax, "range =", rangeMax-rangeMin)

    # gaussian blur
    kernel = generate_gaussian_filer(sigma = 0.6, filter_size = 10)
    curvatureArea_blurred = gaussian_blur(curvatureArea, kernel)
    mpl_regenerateGrayImg(curvatureArea_blurred, "curvatureArea_blurred")

    # # bucket - bug 
    # mpl_regenerateGrayImg(bucketFilter(curvatureArea), "curvatureArea_bucket")

    binary_threshold = 160
    findThres(curvatureArea, binary_threshold)
    curvatureArea_thres = np.where(curvatureArea_blurred < binary_threshold, 0, 255)
    mpl_regenerateGrayImg(curvatureArea_thres, "curvatureArea_blurred_thres0")

    for i in range(170, 250, 10):
        print(i)
        findThres(curvatureArea, i)
        curvatureArea_thres = np.where(curvatureArea_blurred < i, 0, 255)
        mpl_regenerateGrayImg(curvatureArea_thres, "curvatureArea_blurred_thres_"+str(i))

    # intensity_matrix_thres = np.where(intensity_matrix < binary_threshold, 0, 255)
    # mpl_regenerateGrayImg_mpl(intensity_matrix_thres, "intensity_matrix_thres")


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

def test_gaussian_blur():
    arr = np.array([[1,2,4,2,1],
                    [2,4,8,4,2],
                    [4,8,16,8,4],
                    [2,4,8,4,2],
                    [1,2,4,2,1]])
    kernel = generate_gaussian_filer(sigma = 1, filter_size = 3)
    processed_matrix = gaussian_blur(arr, kernel)
    mpl_regenerateGrayImg(arr, "test_gaussian_blur_1")
    mpl_regenerateGrayImg(processed_matrix, "test_gaussian_blur_2")

if __name__ == '__main__':
    # testFilePath = "labData/2023_09_29_Image Data_FW\SP_USAF1951_Gr5-Ele1_H.csv"
    # testFilePath = "labData/2023_09_29_Image Data_FW\PFO-BPy VF-MCE_FS-32_C-wave_575nm_20mW_700-1500nm_Slit100_fall_Vis_F-lens_Trans_1sec_P1_2D.csv"
    # main(testFilePath)
    getCurvatureSample()

    print("Finished")
