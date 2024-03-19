import matplotlib.pyplot as plt
import numpy as np

from process.constants import square
'''
plot curve fit data generated in curvatureDetection.curveFit()
'''
def plot_peak_curve(fig : plt.figure.__class__, 
             max_index : list, max_eV : list):
    
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(max_index, max_eV)
    ax.set_xlabel('Pixel')
    ax.set_ylabel('Energy (eV)')

    fit_ylim_ini = 1.05
    fit_ylim_las = 1.2

    ax.set_ylim(fit_ylim_ini,fit_ylim_las)
    return fig


def plot_parabola_overlay(fig, max_index, max_eV, parabola):
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(max_index, max_eV)
    ax.plot(max_index, parabola)
    ax.set_xlabel('Pixel')
    ax.set_ylabel('Energy (eV)')


'''
plot 2D raw data but cropped
'''
def plot_cropData(fig : plt.figure.__class__, data, wl, startingPx):
    fig.clear()
    ax = fig.add_subplot(111)

    ax.set_ylabel("pixels")
    ax.set_xlabel("wavelength [nm]")
    c = ax.imshow(data, cmap ='jet') 

    fig.colorbar(c, label = "intensity", orientation ='horizontal', fraction=0.13)

    rowCount, colCount = data.shape
    # set y axies as cropped wavelegnth
    wl_interval = 2000 
    wl_vals = [round(v, 2) for v in wl][0::wl_interval]
    ax.set_xticks(np.arange(0, colCount, wl_interval))
    ax.set_xticklabels(wl_vals)

    # set x axies (pixel) start range
    pixel_range = np.arange(startingPx[0], startingPx[1])
    pixel_interval = int((startingPx[1] - startingPx[0])/6)
    pixel_vals = pixel_range[0::pixel_interval]
    ax.set_yticks(np.arange(0, rowCount, pixel_interval))
    ax.set_yticklabels(pixel_vals)

    ax.set_aspect("auto")


'''
plot 2D raw data imported from csv file
'''
def plot_rawData(fig : plt.figure.__class__, data, wl, vmax, vmin):
        fig.clear()
        ax = fig.add_subplot(111)

        ax.set_ylabel("pixels")
        ax.set_xlabel("wavelength [nm]")

        # upperBound, lowerBound = filter_value_bounds(data) 
        # c = ax.imshow(data, cmap ='gray', 
        #             origin='lower', vmin = upperBound, vmax = lowerBound) 
        c = ax.imshow(data, cmap ='jet', vmax = vmax, vmin = vmin) 

        fig.colorbar(c, label = "intensity", orientation ='horizontal', fraction=0.13)

        rowCount, colCount = data.shape
        # set y axies as wavelegnth
        interval = 2000 
        wl_intervaled = [round(v, 2) for v in wl][0::interval]
        ax.set_xticks(np.arange(0, colCount, interval))
        ax.set_xticklabels(wl_intervaled)

        # set x axies (pixel) start range
        num_x_tics = 6
        pixel_range = np.arange(0, rowCount)
        pixel_interval = int((rowCount)/num_x_tics)
        pixel_vals = [round(v, 2) for v in pixel_range][0::pixel_interval]

        ax.set_yticks(np.arange(0, rowCount, pixel_interval))
        ax.set_yticklabels(pixel_vals)

        ax.set_aspect("auto")


# data processing
# filter image to have the desired intensity range
def bound_intensity_value(
        imgArr : np.array.__class__, range : tuple):
    newArr = []
    for pixel in imgArr:
        newPixelVals = []
        for val in pixel:
            if (val < range[0]): 
                newPixelVals.append(range[0])
            elif(val > range[1]):
                newPixelVals.append(range[1])
            else:
                newPixelVals.append(val)
        newArr.append(newPixelVals)
    
    return newArr


def findClosestData(value, dataSet) -> int:
    index = 0
    for ind, val in enumerate(dataSet):
        if (val < value):
            continue
        else:
            index = ind
            break

    return index