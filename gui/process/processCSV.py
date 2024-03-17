import csv 
import numpy as np

CONVERTION_PATH = "../resource/pixel_to_k.csv"

#####################################################
# CSV processing
#####################################################
def get_csv_data(filePath : str):
    file_data = []
    matrix_data = []
    skipHeaderRows = 4
    skipFooterRows = 4
    try:
        print("LOG data extraction successful...\n")
        with open(filePath, 'r') as file:
            reader = csv.reader(file)    
            for row in reader:
                file_data.append(row[1:])
    except FileNotFoundError:
        print("ERR cannot find file \n")
        return


    while skipFooterRows > 0:
        del file_data[-1]
        skipFooterRows -= 1

    while skipHeaderRows > 0:
        file_data.pop(0)
        skipHeaderRows -= 1


    for row in file_data:
        matrix_data.append(np.array(row, dtype = int))

    print(f"Finish retrieving data from csv \n{filePath}\n")
    return matrix_data


def get_csv_wavelength(filePath : str):
    waveLengthData = []
    with open(filePath, 'r') as file:
        reader = csv.reader(file)    
        for row in reader:
            if (row[0] == "Wavelength"):
                waveLengthData = row[1:].copy()
                break
    # pixelData
    return list(map(float, waveLengthData))


def store_as_csv(name, arr):
    np.savetxt("output_curvature/" + name + ".csv", arr, delimiter=",")


def write_detection_result(valid_curves):
    conv_data = read_conversion_data(CONVERTION_PATH)
    with open('./output_log/detectionResults.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['vertial stretch', 'center-y [nm]', 'center-x [pixels]', 'center-x [k-bar]'])
        for entry in valid_curves:
            row = [entry[0], entry[1], entry[2]]
            row.append(conv_data[entry[2]][1])
            writer.writerow(row)


# each entry: [0] = Pixel, [1] = θ1 (°), [2] = K||(m-1)
def read_conversion_data(filePath, list_layout = 0):
    if list_layout == 1:
        entry_list = []
        with open(filePath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                entry_list.append([float(i) for i in row])
        return entry_list

    pixel_map = {}
    with open(filePath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            pixel_map[int(row[0])] = (float(row[1]), float(row[2]))

    return pixel_map


def conver_pixel2kbar(pixel, conversion_data):
    return conversion_data[pixel]


def save_csv(data : list, name : str):
    pass