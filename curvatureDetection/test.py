from curvature_analysis_helper import *

def test_read_conersion_data():
    conversionPath = r'pixel_to_k.csv'
    print(read_conversion_data(conversionPath))


def test_plot_rawData():
    path = r"C:\Users\James\Documents\UWaterloo\QuIN\QuIN - GitHub\imageAnalysis\labData\2023_11_15_Image Data-new_FW\2023_11_15_Image Data-new_FW\FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv"
    data = get_csv_data(path)
    wl = get_csv_wavelength(path)
    fig = plot_rawData(np.array(data), np.array(wl))
    fig.show()

if __name__ == '__main__':
    # pass
    test_plot_rawData()
