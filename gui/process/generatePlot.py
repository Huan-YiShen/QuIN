import matplotlib.pyplot as plt
import numpy as np

def plot_cropData():
    pass

def plot_rawData(fig : plt.figure.__class__, data, wl):
        fig.clear()
        plot = fig.add_subplot(111)

        # mpl_regenerateGrayImg(img, "noCurve")
        plot.set_ylabel("pixels")
        plot.set_xlabel("wavelength [nm]")

        # upperBound, lowerBound = filter_value_bounds(data) 
        # c = plot.imshow(data, cmap ='gray', 
        #             origin='lower', vmin = upperBound, vmax = lowerBound) 
        c = plot.imshow(data, cmap ='gray') 

        fig.colorbar(c, label = "intensity", orientation ='horizontal', fraction=0.13)

        # set y axies as wavelegnth
        _, colCount = data.shape
        interval = 2000 
        wl_intervaled = [round(v, 2) for v in wl][0::interval]
        plot.set_xticks(np.arange(0, colCount, interval))
        plot.set_xticklabels(wl_intervaled)
        plot.set_aspect("auto")

# data processing
def filter_value_bounds(imgArr : np.array.__class__):
    print(imgArr)
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


def findClosestData(value, dataSet) -> int:
    index = 0
    for ind, val in enumerate(dataSet):
        if (val < value):
            continue
        else:
            index = ind
            break

    return index