import tkinter as tk
import ntpath
import numpy as np
import re
import matplotlib.pyplot as plt

from frame.FrameCanvas import FrameCanvas
from process.generatePlot import *

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class FrameImageCrop(tk.Frame):
    def __init__(self, parent, data = [], wl = []):
        super().__init__(parent)
        # data variables
        self.raw_data = data
        self.raw_wl = wl
        self.crop_data = []
        self.crop_wl = []
        # input internal variables
        self.cropPixelRange = tk.StringVar(value = "[min, max]")
        self.cropWlRange = tk.StringVar(value = "[min, max]")
        self.cropIntensityRange = tk.StringVar(value = "[min, max]")
        self.fig = plt.figure(dpi = 100)
        self.create_widgets()
        self.place_widgets()


    def update(self, data, wl):
        self.raw_data = data
        self.raw_wl = wl


    def setCropped(self, data, wl):
        self.crop_data = data
        self.crop_wl = wl


    def crop(self):
        if (self.raw_data is None or self.raw_wl is None):
            print("ERR import data first")
            return
        
        # get cropping values
        cpMin, cpMax = (0, len(self.raw_data))
        cwMin, cwMax = (self.raw_wl[0], self.raw_wl[-1])
        ciMin, ciMax = (np.amin(self.raw_data), np.amax(self.raw_data))

        pixAllNums = [int(s) for s in re.findall(r'\d+', self.cropPixelRange.get())]
        if (len(pixAllNums) == 2): cpMin, cpMax = pixAllNums[:2]

        wlAllNums = [float(s) for s in re.findall(r'\d+', self.cropWlRange.get())]
        if (len(wlAllNums) == 2): 
            cwMin, cwMax = wlAllNums[:2]

        itAllNums = [int(s) for s in re.findall(r'\d+', self.cropIntensityRange.get())]
        if (len(itAllNums) == 2): ciMin, ciMax = itAllNums[:2]

        #debug
        print(f'''LOG data extracted:
              crop pixel range = {cpMin, cpMax}
              crop wavelength range = {cwMin, cwMax}
              crop intensity range = {ciMin, ciMax}''')

        # crop pixel and wl
        lw_index_min = findClosestData(cwMin, self.raw_wl)
        wl_index_max = findClosestData(cwMax, self.raw_wl)
        
        mask = np.ix_(np.arange(cpMin, cpMax), np.arange(lw_index_min, wl_index_max))
        print(cwMax)
        print(self.raw_wl)
        print(cpMin, cpMax, lw_index_min, wl_index_max)
        print("===")
        print(mask)
        self.setCropped(
            data = np.array(np.array(self.raw_data)[mask]),
            wl = np.array(self.raw_wl[lw_index_min : wl_index_max]))

        # crop intensity - set upper and lower bounds

        # plot data
        # try:
        print("LOG generating cropped figure...\n")
        plot_rawData(self.fig, self.crop_data, self.crop_wl)
        self.f_plot.updateCanvas()
        # self.fig.subplots_adjust(left = -1, bottom = 0.13)
        # plt.show() #################################################### DEBUG
        # except:
        #     print("ERR cannot plot raw data \n")
        #     return


    def create_widgets(self):
        self.lb_title = tk.Label(self, text = "Crop Image")
        self.f_para = tk.Frame(self)
        self.generate_parameter_frame(self.f_para)
        self.f_plot = FrameCanvas(self, self.fig)
        

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

        en_cPixelRange = tk.Entry(frame, textvariable=self.cropPixelRange)
        en_cWlRange = tk.Entry(frame, textvariable=self.cropWlRange)
        en_cIntensityRange = tk.Entry(frame, textvariable=self.cropIntensityRange)
        
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
