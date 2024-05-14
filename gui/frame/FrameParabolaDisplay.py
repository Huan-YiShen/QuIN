import tkinter as tk
from tkinter import ttk

from process.constants import square
from process.constants import pixel2angle_linear
from process.constants import angle2k_ll
from process.generatePlot import plot_parabola_overlay
from frame.FrameCanvas import FrameCanvas
from frame.dataStruct import parabolaData

import numpy as np
import matplotlib.pyplot as plt


class FrameParabolaDisplay(tk.Frame):
    def __init__(self, parent, data : parabolaData):
        super().__init__(parent)
        self.fc_curve_pixel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.fc_curve_angle = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.fc_curve_kParallel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))

        self.data = data

        # self.peak_fitting()
        self.place_widgets()


    def get_data(self):
        return self.data

    def update(self, max_index, max_eV, crop_index, parabola, parabolaVertex):
        self.data.base_x = max_index
        self.data.base_y = max_eV
        self.data.parabola_x = crop_index
        self.data.parabola_y = parabola

        print("update FrameParabolaDisplay")
        plot_parabola_overlay(
            fig = self.fc_curve_pixel.fig, 
            base_x = self.data.base_x, 
            base_y = self.data.base_y,
            parabola_x = self.data.parabola_x, 
            parabola = self.data.parabola_y)
        
        self.data.base_angles = pixel2angle_linear(
            self.data.base_x, parabolaVertex)
        self.data.parabola_angles = pixel2angle_linear(
            self.data.parabola_x, parabolaVertex)

        plot_parabola_overlay(
            fig = self.fc_curve_angle.fig, 
            base_x = self.data.base_angles,
            base_y = self.data.base_y,
            parabola_x = self.data.parabola_angles,
            parabola = self.data.parabola_y,
            x_label = "angle")
        
        # TODO currently hard coded to convert m to um 
        self.data.base_kpara = angle2k_ll(self.data.base_angles)*1e-6
        self.data.parabola_kpara = angle2k_ll(self.data.parabola_angles)*1e-6

        plot_parabola_overlay(
            fig = self.fc_curve_kParallel.fig, 
            base_x = self.data.base_kpara,
            base_y = self.data.base_y,
            parabola_x = self.data.parabola_kpara,
            parabola = self.data.parabola_y,
            x_label = r'k$_{||} (\mu m^{-1}$)')


        self.fc_curve_pixel.updateCanvas()
        self.fc_curve_angle.updateCanvas()
        self.fc_curve_kParallel.updateCanvas()


    def place_widgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.fc_curve_pixel.grid(row = 0, column= 0, sticky="news")
        self.fc_curve_angle.grid(row = 0, column = 1, sticky="news")
        self.fc_curve_kParallel.grid(row = 0, column = 2, sticky="news")
