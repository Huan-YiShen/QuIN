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
        # initialize variables

        # data variables (initial data)
        self.filePath = path
        self.data = data
        self.wl = wl

        # display variables
        self.fileName = tk.StringVar()
        self.pixelRange = tk.StringVar()
        self.wlRange = tk.StringVar()
        self.intensityMax = tk.StringVar()
        self.intensityMin = tk.StringVar()
        self.fig = plt.figure(dpi = 100)

        # widget variables
        self.create_widgets()
        self.place_widgets()


    def create_widgets(self):
        # title label widget
        self.lb_title = tk.Label(self, text = "Import Full Image")
        # parameter frame widget
        self.f_stat = tk.Frame(self)
        self.generate_parameter_frame()
        # canvas frame widget
        self.f_plot = FrameCanvas(self, self.fig)


    def update(self, path, data, wl):
        self.filePath = path
        self.data = data
        self.wl = wl

        self.fileName.set(path_leaf(path))
        self.pixelRange.set(f"0 ~ {len(data)}")
        self.wlRange.set(f"{round(self.wl[0], 2)} ~ {round(self.wl[-1], 2)}")
        
        maxIntensity = np.amax(data)
        minIntensity = np.amin(data)
        self.intensityMax.set(maxIntensity)
        self.intensityMin.set(minIntensity)

        # Intensity Data: enable edit and bind to update_graph_intensity
        self._en_intensityMax.configure(state="normal")
        self._en_intensityMin.configure(state="normal")
        self._en_intensityMax.bind('<Return>', self._update_graph_intensity)
        self._en_intensityMin.bind('<Return>', self._update_graph_intensity)

        #debug log
        print(f'''LOG data extracted:
              self.fileName = {self.fileName}
              self.pixelRange = {self.pixelRange}
              self.wlRange = {self.wlRange}
              self.intensityMax = {self.intensityMax}
              self.intensityMin = {self.intensityMin}''')

        # plot data
        try:
            print("LOG generating full figure...\n")
            plot_rawData(
                self.fig, np.array(self.data), np.array(self.wl), 
                float(maxIntensity), float(minIntensity))
            self.f_plot.updateCanvas()
            # plt.show() #################################################### for DEBUG
        except Exception as e:
            print(f"ERR cannot plot raw data \n\t {e}")
            return


    def _update_graph_intensity(self, *args):
        print(f'''update intensity:
            self.intensityMax = {self.intensityMax}
            self.intensityMin = {self.intensityMin}''')
        # replot
        try:
            print("LOG generating figure...")
            plot_rawData(
                self.fig, np.array(self.data), np.array(self.wl), 
                float(self.intensityMax.get()), float(self.intensityMin.get()))
            self.f_plot.updateCanvas()
            # plt.show() #################################################### DEBUG
        except Exception as e:
            print("ERR cannot plot raw data \n\t {e}")
            return
        

    def get_intensity_data(self):
        return(self.intensityMin, self.intensityMin)


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
        self._en_intensityMax = tk.Entry(self.f_stat, textvariable=self.intensityMax, state= "readonly")
        self._en_intensityMin = tk.Entry(self.f_stat, textvariable=self.intensityMin, state= "readonly")

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
        self._en_intensityMax.grid(row = 3, column= 1, sticky="we")
        self._en_intensityMin.grid(row = 4, column= 1, sticky="we")
