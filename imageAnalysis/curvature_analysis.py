import numpy as np
import matplotlib.pyplot as plt
import csv

#####################################################
# image processing
#####################################################
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

def mpl_regenerateGrayImg(arr, name):
        plt.figure()
        plt.imshow(arr, cmap = 'gray', origin='lower')
        desnPath = "./output_curvature/" + name + ".png"
        plt.savefig(desnPath)
        return desnPath

#####################################################
# CSV processing
#####################################################
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


def get_csv_wavelength(filePath):
    waveLengthData = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file)    
        for row in reader:
            # if (row[0] == "Column"):
            #     pixelData = row[1:].copy()
            if (row[0] == "Wavelength"):
                waveLengthData = row[1:].copy()
                break
    # pixelData
    return list(map(float, waveLengthData))


def store_as_csv(name, arr):
    np.savetxt("output_curvature/" + name + ".csv", arr, delimiter=",")


#####################################################
# Gaussian Blur
#####################################################
# filter_size = length of the square filter
# kernel generatino
def generate_gaussian_filer(sigma, filter_size):

    m_half = filter_size // 2
    n_half = filter_size // 2

    # initializing the filter
    gaussian_filter = np.zeros((filter_size, filter_size), np.float32)
    normal = 1 / (2 * np.pi * (sigma*sigma))

    # generating the filter
    for y in range(-m_half, m_half):
        for x in range(-n_half, n_half):
            exp_term = np.exp(-(x*x + y*y) / (2.0 * sigma*sigma))
            gaussian_filter[y+m_half, x+n_half] = normal * exp_term
    print("producted gaussian filter:")
    print(gaussian_filter)
    return gaussian_filter


def convolution(src, kernel):
    ver_s, hor_s = src.shape
    var_k, hor_k = kernel.shape

    if (ver_s != var_k): return 0
    if (hor_s != hor_k): return 0

    sol = 0
    for ind_y, row in enumerate(src):
        for ind_x, val in enumerate(row):
            sol += val*kernel[ind_y][ind_x]

    return sol


def gaussian_blur(src : np.ndarray, kernel : np.ndarray) -> np.array:
    mean_s = src.mean()
    print("mean: ", mean_s)
    ver_s, hor_s = src.shape
    ver_k, hor_k = kernel.shape
    print("kernel size: vertical =", ver_k, ", horizontal =", hor_k)
    print("source size: vertical =", ver_k, ", horizontal =", hor_k)

    if (ver_k != hor_k): return 0
    print("performing Gaussian Blur...")
    padding = int(ver_k/2)
    padded_src_size = (ver_s+2*padding, hor_s+2*padding)
    padded_src = np.zeros(padded_src_size, np.float32)
    for ind, row in enumerate(padded_src[padding:(-padding)]):
        row[padding:(-padding)] = src[ind].copy()
    print("padding = ", padding)
    print(padded_src)
    
    res = np.zeros(src.shape, np.float32)
    
    for ind_y, row in enumerate(src):
        # each pixel of the the result will be a convolution of the src and kernel
        for ind_x, _ in enumerate(row):
            # get submatrix
            srcSub = np.zeros(kernel.shape, np.float32)
            padded_rows = padded_src[ind_y : ind_y + ver_k]
            for i, pad_row in enumerate(padded_rows):
                srcSub[i] = pad_row[ind_x : ind_x + hor_k].copy()
            res[ind_y][ind_x] = convolution(srcSub, kernel)

    print(res+mean_s)
    return res


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

#####################################################
# Bucket Filter
#####################################################
def bucketFilter(curvatureArea):
    pass 
    # old analysis
    # # min = -2360 max = 4579 range = 6939
    # min = -23
    # max = 47
    # bucket = np.arange(min, max)
    # # rangeVal = max-min
    # # step = 255/rangeVal

    # res = np.zeros(curvatureArea.shape, np.float32)
    # for y, row in enumerate(curvatureArea):
    #     for x, entry in enumerate(row):
    #         for val in bucket:
    #             if (entry < val):
    #                 res[y][x] = int(entry/100) + 1
    #                 break 
    # return res

def filter_value_bounds(imgArr):
    # bin
    bins = 10000
    countThres = 100 # if there is <countThres number of pixel, bound will change
    
    hist, binRange = np.histogram(imgArr.flatten(), bins = bins)
    lowerBound = np.min(imgArr)
    upperBound = np.max(imgArr)
    print("min = ", lowerBound, "max = ", upperBound, "range = ", upperBound-lowerBound)

    for index, val in enumerate(hist):
        if(val < countThres): lowerBound = binRange[index+1]
        else: break
    ind = bins
    for val in hist[::-1]:
        if (val < countThres): upperBound = binRange[ind]
        else: break
        ind -= 1

    if (lowerBound == np.max(imgArr) or upperBound == np.min(imgArr)):
        lowerBound, upperBound = upperBound, lowerBound

    print("lowerThres = {:0.2f} UppwerThres = {:0.2f} Range = {:0.2f}".format(lowerBound, upperBound, upperBound-lowerBound))
    return upperBound, lowerBound

#####################################################
# other analysis
#####################################################
def relative_value(intensity_data : np.ndarray) -> np.ndarray:
    max_val = np.amax(intensity_data)
    min_val = np.amin(intensity_data)
    print("max_val = ", max_val, ", min_val = ", min_val)
    adjustment_ratio = 255/(max_val - min_val)
    # intensity_data = intensity_data + abs(min_val)
    return intensity_data
    # return (intensity_data*adjustment_ratio).round().astype(int)

