import matplotlib.pyplot as plt
import numpy as np

def plot_cropData(fig : plt.figure.__class__, data, wl, startingPx):
    fig.clear()
    plot = fig.add_subplot(111)

    plot.set_ylabel("pixels")
    plot.set_xlabel("wavelength [nm]")
    c = plot.imshow(data, cmap ='jet') 

    fig.colorbar(c, label = "intensity", orientation ='horizontal', fraction=0.13)

    rowCount, colCount = data.shape
    # set y axies as cropped wavelegnth
    wl_interval = 2000 
    wl_vals = [round(v, 2) for v in wl][0::wl_interval]
    plot.set_xticks(np.arange(0, colCount, wl_interval))
    plot.set_xticklabels(wl_vals)

    # set x axies (pixel) start range
    pixel_range = np.arange(startingPx[0], startingPx[1])
    pixel_interval = int((startingPx[1] - startingPx[0])/6)
    pixel_vals = pixel_range[0::pixel_interval]
    plot.set_yticks(np.arange(0, rowCount, pixel_interval))
    plot.set_yticklabels(pixel_vals)

    plot.set_aspect("auto")


def plot_rawData(fig : plt.figure.__class__, data, wl, vmax, vmin):
        fig.clear()
        plot = fig.add_subplot(111)

        plot.set_ylabel("pixels")
        plot.set_xlabel("wavelength [nm]")

        # upperBound, lowerBound = filter_value_bounds(data) 
        # c = plot.imshow(data, cmap ='gray', 
        #             origin='lower', vmin = upperBound, vmax = lowerBound) 
        c = plot.imshow(data, cmap ='jet', vmax = vmax, vmin = vmin) 

        fig.colorbar(c, label = "intensity", orientation ='horizontal', fraction=0.13)

        rowCount, colCount = data.shape
        # set y axies as wavelegnth
        interval = 2000 
        wl_intervaled = [round(v, 2) for v in wl][0::interval]
        plot.set_xticks(np.arange(0, colCount, interval))
        plot.set_xticklabels(wl_intervaled)

        # set x axies (pixel) start range
        num_x_tics = 6
        pixel_range = np.arange(0, rowCount)
        pixel_interval = int((rowCount)/num_x_tics)
        pixel_vals = [round(v, 2) for v in pixel_range][0::pixel_interval]

        plot.set_yticks(np.arange(0, rowCount, pixel_interval))
        plot.set_yticklabels(pixel_vals)

        plot.set_aspect("auto")


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