import tkinter as tk
from tkinter import ttk

from process.constants import square
from process.curvatureDetection import peak_curve
from process.generatePlot import plot_peak_curve
from process.generatePlot import plot_parabola_overlay
from process.curvatureDetection import find_parabola
from frame.FrameCanvas import FrameCanvas
from frame.FrameParabolaDisplay import FrameParabolaDisplay

import numpy as np
import matplotlib.pyplot as plt

class FrameParabolaDetect(tk.Frame):
    def __init__(self, parent,
                 data, wl, initPixelVal, displayFrame = FrameParabolaDisplay.__class__):

        super().__init__(parent)
        self.config(borderwidth = 1)

        self.data = data
        self.wl = wl
        self.initPixelVal = initPixelVal
        self.displayFrame = displayFrame

        # for full frame
        self.parabolaVertex = 0
        self.parabola = None
        self.max_index = None
        self.max_wl = None
        self.max_eV = None

        # for crop frame
        self.crop_pixelMin = tk.IntVar()
        self.crop_pixelMax = tk.IntVar()
        self.crop_index = None
        self.crop_eV = None

        self.f_curve_full = None
        self.f_curve_crop_overlay = None

        self.create_widgets()
        self.peak_fitting()
        self.place_widgets()


    def peak_fitting(self):
        self.max_index, self.max_wl, self.max_eV = peak_curve(self.data, self.wl)
        self.max_index = np.array(self.max_index) + self.initPixelVal # since data is cropped

        popt = find_parabola(self.max_index, self.max_eV)
        self.parabola = square(self.max_index, popt[0], popt[1], popt[2])
        self.parabolaVertex = popt[1]

        plot_parabola_overlay(
            fig = self.f_curve_full.fig, 
            base_x = self.max_index, 
            base_y = self.max_eV, 
            parabola_x = self.max_index, 
            parabola = self.parabola)
        self.f_curve_full.updateCanvas()

        self.crop_index = self.max_index
        self.crop_eV = self.max_eV
        self.crop_pixelMin.set(self.initPixelVal)
        self.crop_pixelMax.set(self.max_index[-1])
    
        self.displayFrame.update(
            self.max_index, self.max_eV, 
            self.crop_index, self.parabola,
            self.parabolaVertex)


    def create_widgets(self):
        self.create_full_widget()
        self.create_crop_widget()


    def create_full_widget(self):
        self.f_full = tk.Frame(self)
        self.f_curve_full = FrameCanvas(
            self.f_full, plt.figure(dpi = 100), size = (640, 320), toolBar=True)

        lb_control = tk.Label(self.f_full, text = "Max intensity at each pixel")

        lb_control.grid(row = 0, column = 0, sticky= "we")
        self.f_curve_full.grid(row = 1, column = 0, sticky= "we")


    def create_crop_widget(self):
        # create crop wiget
        self.f_crop = tk.Frame(self)
        self.f_curve_crop_overlay = FrameCanvas(
            self.f_crop, plt.figure(dpi = 100), size = (640, 320), toolBar=False)

        # self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
        #                 text="Click the bubbles that are multiples of two.")

        # finer crop control frame
        f_control = tk.Frame(self.f_crop)

        lb_control = tk.Label(f_control, text = "Finer Pixel Crop Control (press <Enter-key> to crop)")
        lb_pixelMin = tk.Label(f_control, text = "Pixel Min")
        lb_pixelMax = tk.Label(f_control, text = "Pixel Max")
        en_pixelMin = tk.Entry(f_control, textvariable=self.crop_pixelMin)
        en_pixelMax = tk.Entry(f_control, textvariable=self.crop_pixelMax)
        en_pixelMin.bind('<Return>', self._update_plot)
        en_pixelMax.bind('<Return>', self._update_plot)

        # placement
        lb_control.grid(row = 0, column = 0, columnspan = 4)
        lb_pixelMin.grid(row = 1, column= 0, padx=20, sticky="w")
        en_pixelMin.grid(row = 1, column= 1, sticky="we")
        lb_pixelMax.grid(row = 1, column= 2, padx=20, sticky="w")
        en_pixelMax.grid(row = 1, column= 3, sticky="we")

        # next step button
        btn_display = ttk.Button(
            master = self.f_crop, text = "Update Display",
            command = lambda:self.displayFrame.update(
                self.max_index, self.max_eV, 
                self.crop_index, self.parabola,
                self.parabolaVertex))


        f_control.grid(row = 0, column = 0)
        self.f_curve_crop_overlay.grid(row = 1, column = 0, sticky = "news")
        btn_display.grid(row = 2, column = 0, sticky = "ew")


    def _update_plot(self, *arg):
        minOffseted = self.crop_pixelMin.get()-self.initPixelVal
        maxOffseted = self.crop_pixelMax.get()-self.initPixelVal
        self.crop_index = self.max_index[minOffseted : maxOffseted]
        self.crop_eV = self.max_eV[minOffseted : maxOffseted]

        popt = find_parabola(self.crop_index, self.crop_eV)
        self.parabola = square(self.crop_index, popt[0], popt[1], popt[2])
        self.parabolaVertex = popt[1]
        plot_parabola_overlay(
            fig = self.f_curve_crop_overlay.fig, 
            base_x = self.crop_index, 
            base_y = self.crop_eV, 
            parabola_x = self.crop_index, 
            parabola = self.parabola)

        self.f_curve_crop_overlay.updateCanvas()


    def place_widgets(self):
        self.columnconfigure(2, weight=1)
        self.f_full.grid(row = 0, column = 0, sticky = "news")
        self.f_crop.grid(row = 0, column = 1, sticky = "news")
