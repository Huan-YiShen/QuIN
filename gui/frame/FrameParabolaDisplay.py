import tkinter as tk
from tkinter import ttk

from process.constants import square
from process.constants import pixel2angle_linear
from process.constants import angle2k_ll
from process.generatePlot import plot_parabola_overlay
from frame.FrameCanvas import FrameCanvas

import numpy as np
import matplotlib.pyplot as plt

class FrameParabolaDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.f_curve_pixel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.f_curve_angle = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.f_curve_kParallel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))

        # self.peak_fitting()
        self.place_widgets()


    def update(self, max_index, max_eV, crop_index, parabola, parabolaVertex):
        print("update FrameParabolaDisplay")
        plot_parabola_overlay(
            fig = self.f_curve_pixel.fig, 
            base_x = max_index, 
            base_y = max_eV,
            parabola_x = crop_index, 
            parabola = parabola)

        self.angles = pixel2angle_linear(max_index, parabolaVertex)
        self.crop_angles = pixel2angle_linear(crop_index, parabolaVertex)

        plot_parabola_overlay(
            fig = self.f_curve_angle.fig, 
            base_x = self.angles,
            base_y = max_eV,
            parabola_x = self.crop_angles,
            parabola = parabola,
            x_label = "angle")
        
        # TODO currently hard coded to convert m to um 
        self.kpara = angle2k_ll(self.angles)*1e-6
        self.crop_kpara = angle2k_ll(self.crop_angles)*1e-6

        plot_parabola_overlay(
            fig = self.f_curve_kParallel.fig, 
            base_x = self.kpara, 
            base_y = max_eV, 
            parabola_x = self.crop_kpara, 
            parabola = parabola,
            x_label = r'k$_{||} (\mu m^{-1}$)')


        self.f_curve_pixel.updateCanvas()
        self.f_curve_angle.updateCanvas()
        self.f_curve_kParallel.updateCanvas()


    def place_widgets(self):
        self.columnconfigure(3, weight=1)
        self.f_curve_pixel.grid(row = 0, column= 0, sticky="news")
        self.f_curve_angle.grid(row = 0, column = 1, sticky="news")
        self.f_curve_kParallel.grid(row = 0, column = 2, sticky="news")
