import tkinter as tk
from tkinter import ttk

from process.curvatureDetection import curveFit
from process.generatePlot import plot_curveFit
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
        # create_widgets()
        self.f_peakPlot = FrameCanvas(self, plt.figure(dpi = 100), 
                                      size = (320, 320), toolBar=True)
        self.f_cropPlot = FrameCanvas(self, plt.figure(dpi = 100), 
                                      size = (640, 640), toolBar=True)
        self.f_detectedPlot = FrameCanvas(self, plt.figure(dpi = 100), 
                                      size = (320, 320), toolBar=True)

        self.peak_fitting()
        self.place_widgets()



    def peak_fitting(self):
        self.max_index, self.max_wl, self.max_eV = curveFit(self.data, self.wl)
        self.max_index = np.array(self.max_index) + self.initPixelVal # since data is cropped

        plot_curveFit(self.f_peakPlot.fig, self.max_index, self.max_eV)
        self.f_peakPlot.updateCanvas()

        popt = find_parabola(self.max_index, self.max_eV)
        plot_parabola_overlay(self.f_detectedPlot.fig, self.max_index, self.max_eV, popt)
        self.f_detectedPlot.updateCanvas()


    def place_widgets(self):
        self.f_peakPlot.pack()
        self.f_detectedPlot.pack()