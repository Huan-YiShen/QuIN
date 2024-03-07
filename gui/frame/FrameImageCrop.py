import tkinter as tk
import ntpath
import numpy as np
import re
import matplotlib.pyplot as plt

from frame.FrameCanvas import FrameCanvas
from process.generatePlot import findClosestData
from process.generatePlot import bound_intensity_value
from process.generatePlot import plot_cropData


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class FrameImageCrop(tk.Frame):
    def __init__(self, parent, data = [], wl = []):
        super().__init__(parent)
        # initialize variables
        # data variables (initial data)
        self.raw_data = data
        self.raw_wl = wl

        # display variables
        self.displayPixelRange = tk.StringVar(value = "[min, max]")
        self.displayWlRange = tk.StringVar(value = "[min, max]")
        self.displayIntensityRange = tk.StringVar(value = "[min, max] do not modify until top two are set")

        # state variables (storing post processing)
        self.crop_data = []
        self.crop_wl = []
        self.crop_pixels = (0, 0)             # could store only starting pixel so we can get the ending via crop_data row count
        self.crop_intensity = (0, 0)
        self.fig = plt.figure(dpi = 100)

        # widget variables
        self.create_widgets()
        self.place_widgets()


    def create_widgets(self):
        # title label widget
        self.lb_title = tk.Label(self, text = "Crop Image")
        # parameter frame widget
        self.f_para = tk.Frame(self)
        self.generate_parameter_frame(self.f_para)
        # canvas frame widget
        self.f_plot = FrameCanvas(self, self.fig)


    def update(self, data, wl):
        self.raw_data = data
        self.raw_wl = wl


    def set_displayIntensity(self, intensityMinMax : tuple):
        min, max = intensityMinMax
        self.displayIntensityRange.set(str(min, ", ", max))


    def crop(self):
        if (self.raw_data is None or self.raw_wl is None):
            print("ERR import data first")
            return
        
        # get cropping values
        cpMinMax, cwMinMax, ciMinMax = self._read_display_value()

        # crop pixel and wl
        lw_index_min = findClosestData(cwMinMax[0], self.raw_wl)
        wl_index_max = findClosestData(cwMinMax[1], self.raw_wl)
        mask = np.ix_(np.arange(cpMinMax[0], cpMinMax[1]), np.arange(lw_index_min, wl_index_max))
        # crop intensity - set upper and lower bounds
        croppedFig = bound_intensity_value(
            np.array(self.raw_data)[mask], (ciMinMax[0], ciMinMax[1]))

        ## debug log
        print(f'''FramgeImageCrop.crop():
              cpMin = {cpMinMax[0]}
              cpMax = {cpMinMax[1]}
              lw_index_min = {lw_index_min}
              wl_index_max = {wl_index_max}
              ciMin = {ciMinMax[0]}
              ciMax = {ciMinMax[1]}''')

        # update state variables
        self._set_cropped_var(
            data = np.array(croppedFig),
            wl = np.array(self.raw_wl[lw_index_min : wl_index_max]),
            startingPx = (cpMinMax[0], cpMinMax[1]),
            intensityRange = (ciMinMax[0], ciMinMax[1])
            )

        # plot data
        try:
            print("LOG generating cropped figure...\n")
            plot_cropData(self.fig, self.crop_data, 
                        self.crop_wl, self.crop_pixels)
            self.f_plot.updateCanvas()
            ## plt.show() #################################################### for DEBUG
        except:
            print("ERR cannot plot cropped data \n")
            return


    def _read_display_value(self):
        cpMin, cpMax = (0, len(self.raw_data))
        cwMin, cwMax = (self.raw_wl[0], self.raw_wl[-1])
        ciMin, ciMax = (np.amin(self.raw_data), np.amax(self.raw_data))

        pixAllNums = [int(s) for s in re.findall(r'\d+', self.displayPixelRange.get())]
        if (len(pixAllNums) == 2): cpMin, cpMax = pixAllNums[:2]

        wlAllNums = [float(s) for s in re.findall(r'\d+', self.displayWlRange.get())]
        if (len(wlAllNums) == 2): 
            cwMin, cwMax = wlAllNums[:2]

        itAllNums = [int(s) for s in re.findall(r'\d+', self.displayIntensityRange.get())]
        if (len(itAllNums) == 2): ciMin, ciMax = itAllNums[:2]

        return (cpMin, cpMax), (cwMin, cwMax), (ciMin, ciMax)


    def _set_cropped_var(self, data = [], wl = [], startingPx = (0,0), intensityRange = (0,0)):
        self.crop_data = data
        self.crop_wl = wl
        self.crop_pixels = startingPx
        self.crop_intensity = intensityRange
        

    def place_widgets(self):
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.lb_title.grid(row = 0, column = 0, sticky="nw")
        self.f_para.grid(row = 1, column = 0, sticky="nwe")
        self.f_plot.grid(row = 2, column = 0, sticky="news")


    def generate_parameter_frame(self, frame):
        lb_cPixelRange = tk.Label(frame, text = "Crop Pixel Range")
        lb_cWlRange = tk.Label(frame, text = "Crop λ Range")
        lb_cIntensityRange = tk.Label(frame, text = "Crop Intensity Range")

        en_cPixelRange = tk.Entry(frame, textvariable=self.displayPixelRange)
        en_cWlRange = tk.Entry(frame, textvariable=self.displayWlRange)
        en_cIntensityRange = tk.Entry(frame, textvariable=self.displayIntensityRange)
        
        btn_crop = tk.Button(frame, text = "Crop", command=self.crop)
        #### layout #### 
        frame.columnconfigure(1, weight=1)

        lb_cPixelRange.grid(row = 0, column= 0, padx=20, sticky="w")
        lb_cWlRange.grid(row = 1, column= 0, padx=20, sticky="w")
        lb_cIntensityRange.grid(row = 2, column= 0, padx=20, sticky="w")

        en_cPixelRange.grid(row = 0, column= 1, sticky="we")
        en_cWlRange.grid(row = 1, column= 1, sticky="we")
        en_cIntensityRange.grid(row = 2, column= 1, sticky="we")

        btn_crop.grid(row = 3, column= 0, padx=20, pady=8, sticky="w")
