import tkinter as tk
from tkinter import ttk

from process.constants import square
from process.curvatureDetection import peak_curve
from process.generatePlot import plot_peak_curve
from process.generatePlot import plot_parabola_overlay
from process.curvatureDetection import find_parabola
from frame.FrameCanvas import FrameCanvas

import numpy as np
import matplotlib.pyplot as plt

class FrameParabolaDetect(tk.Frame):
    def __init__(self, parent,
                 data, wl, initPixelVal):

        super().__init__(parent)
        self.data = data
        self.wl = wl
        self.initPixelVal = initPixelVal

        self.max_index = None
        self.max_wl = None
        self.max_eV = None

        self.f_curve_full = FrameCanvas(
            self, plt.figure(dpi = 100), size = (640, 320), toolBar=True)
        self.f_curve_crop_overlay = FrameCanvas(
            self, plt.figure(dpi = 100), size = (640, 320), toolBar=True)

        self.create_widgets()

        self.peak_fitting()
        self.place_widgets()


    def peak_fitting(self):
        self.max_index, self.max_wl, self.max_eV = peak_curve(self.data, self.wl)
        self.max_index = np.array(self.max_index) + self.initPixelVal # since data is cropped

        popt = find_parabola(self.max_index, self.max_eV)
        parabola = square(self.max_index, popt[0],popt[1],popt[2])

        plot_parabola_overlay(self.f_curve_full.fig, self.max_index, self.max_eV, parabola)
        self.f_curve_full.updateCanvas()


    def create_widgets(self):
        self.pixelMin = tk.IntVar()
        self.pixelMax = tk.IntVar()
        
        self.f_crop = tk.Frame(self)
        
        lb_pixelMin = tk.Label(self.f_crop, text = "Pixel Min")
        lb_pixelMax = tk.Label(self.f_crop, text = "Pixel Max")

        en_pixelMin = tk.Entry(self.f_crop, textvariable=self.pixelMin)
        en_pixelMax = tk.Entry(self.f_crop, textvariable=self.pixelMax)
        en_pixelMin.bind('<Return>', self._update_plot)
        en_pixelMax.bind('<Return>', self._update_plot)

        # placement
        lb_pixelMin.grid(row = 0, column= 0, padx=20, sticky="w")
        en_pixelMin.grid(row = 0, column= 1, sticky="we")
        lb_pixelMax.grid(row = 0, column= 2, padx=20, sticky="w")
        en_pixelMax.grid(row = 0, column= 3, sticky="we")


    def _update_plot(self, *arg):
        self.crop_index = self.max_index[self.pixelMin.get() : self.pixelMax.get()]
        self.crop_eV = self.max_eV[self.pixelMin.get() : self.pixelMax.get()]

        popt = find_parabola(self.crop_index, self.crop_eV)
        parabola = square(self.crop_index, popt[0],popt[1],popt[2])
        plot_parabola_overlay(self.f_curve_crop_overlay.fig, self.crop_index, self.crop_eV, parabola)
        self.f_curve_crop_overlay.updateCanvas()


    def place_widgets(self):
        self.f_curve_full.pack()
        self.f_crop.pack()
        self.f_curve_crop_overlay.pack()