import tkinter as tk
import ntpath
import numpy as np
import matplotlib.pyplot as plt

from frame.FrameCanvas import FrameCanvas
from process.generatePlot import plot_rawData

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class FrameImageFull(tk.Frame):
    def __init__(self, parent, path = "", data = [], wl = []):
        super().__init__(parent)
        self.filePath = path
        self.data = data
        self.wl = wl

        self.fileName = tk.StringVar()
        self.pixelRange = tk.StringVar()
        self.wlRange = tk.StringVar()
        self.intensityMax = tk.StringVar()
        self.intensityMin = tk.StringVar()
        self.fig = plt.figure(dpi = 100)

        # label = tk.Label(self, bg="yellow")
        # label.pack(expand=True, fill = "both")
        self.create_widgets()
        self.place_widgets()


    def update(self, path, data, wl):
        self.filePath = path
        self.data = data
        self.wl = wl

        self.fileName.set(path_leaf(path))
        self.pixelRange.set(f"0 ~ {len(data)}")
        self.wlRange.set(f"{round(self.wl[0], 2)} ~ {round(self.wl[-1], 2)}")
        self.intensityMax.set(np.amax(data))
        self.intensityMin.set(np.amin(data))

        #debug log
        print(f'''LOG data extracted:
              self.fileName = {self.fileName}
              self.pixelRange = {self.pixelRange}
              self.wlRange = {self.wlRange}
              self.intensityMax = {self.intensityMax}
              self.intensityMin = {self.intensityMin}''')

        # plot data
        try:
            print("LOG generating figure...\n")
            plot_rawData(self.fig, np.array(self.data), np.array(self.wl))
            self.f_plot.updateCanvas()
            # self.fig.subplots_adjust(left = -1, bottom = 0.13)
            # plt.show() #################################################### DEBUG
        except:
            print("ERR cannot plot raw data \n")
            return


    def create_widgets(self):
        self.lb_title = tk.Label(self, text = "Import Full Image")

        self.f_stat = tk.Frame(self)
        self.generate_parameter_frame()

        self.f_plot = FrameCanvas(self, self.fig)
        

    def place_widgets(self):
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.lb_title.grid(row = 0, column = 0, sticky="nw")
        self.f_stat.grid(row = 1, column = 0, sticky="nwe")
        self.f_plot.grid(row = 2, column = 0, sticky="news")


    def generate_parameter_frame(self):
        lb_fileName = tk.Label(self.f_stat, text = "File Name")
        lb_pixelRange = tk.Label(self.f_stat, text = "Pixel Range")
        lb_wlRange = tk.Label(self.f_stat, text = "λ Range [nm]")
        lb_intensityMax = tk.Label(self.f_stat, text = "Intensity Max")
        lb_intensityMin = tk.Label(self.f_stat, text = "Intensity Mim")

        en_fileName = tk.Entry(self.f_stat, textvariable=self.fileName, state= "readonly")
        en_pixelRange = tk.Entry(self.f_stat, textvariable=self.pixelRange, state= "readonly")
        en_wlRange = tk.Entry(self.f_stat, textvariable=self.wlRange, state= "readonly")
        en_intensityMax = tk.Entry(self.f_stat, textvariable=self.intensityMax, state= "readonly")
        en_intensityMin = tk.Entry(self.f_stat, textvariable=self.intensityMin, state= "readonly")

        #### layout #### 
        self.f_stat.columnconfigure(1, weight=1)

        lb_fileName.grid(row = 0, column= 0, padx=20, sticky="w")
        lb_pixelRange.grid(row = 1, column= 0, padx=20, sticky="w")
        lb_wlRange.grid(row = 2, column= 0, padx=20, sticky="w")
        lb_intensityMax.grid(row = 3, column= 0, padx=20, sticky="w")
        lb_intensityMin.grid(row = 4, column= 0, padx=20, sticky="w")

        en_fileName.grid(row = 0, column= 1, sticky="we")
        en_pixelRange.grid(row = 1, column= 1, sticky="we")
        en_wlRange.grid(row = 2, column= 1, sticky="we")
        en_intensityMax.grid(row = 3, column= 1, sticky="we")
        en_intensityMin.grid(row = 4, column= 1, sticky="we")
