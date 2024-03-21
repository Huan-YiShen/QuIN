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
            self, plt.figure(dpi = 100), size = (600, 320))
        self.f_curve_angle = FrameCanvas(
            self, plt.figure(dpi = 100), size = (600, 320))
        self.f_curve_kParallel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (600, 320))

        # self.create_widgets()

        # self.peak_fitting()
        self.place_widgets()


    def update(self, max_index, max_eV, crop_index, parabola):
        print("update FrameParabolaDisplay")
        plot_parabola_overlay(
            fig = self.f_curve_pixel.fig, 
            base_x = max_index, 
            base_y = max_eV,
            parabola_x = crop_index, 
            parabola = parabola)

        self.angles = pixel2angle_linear(max_index, parabola)
        self.crop_angles = pixel2angle_linear(crop_index, parabola)

        plot_parabola_overlay(
            fig = self.f_curve_angle.fig, 
            base_x = self.angles,
            base_y = max_eV,
            parabola_x = self.crop_angles,
            parabola = parabola,
            x_label = "angle")
        
        # TODO: impl anlge to angle2kParalle_linear
        self.kpara = angle2k_ll(self.angles)
        self.crop_kpara = angle2k_ll(self.crop_angles)
        plot_parabola_overlay(
            fig = self.f_curve_kParallel.fig, 
            base_x = self.kpara, 
            base_y = max_eV, 
            parabola_x = self.crop_kpara, 
            parabola = parabola,
            x_label = "k_||")


        self.f_curve_pixel.updateCanvas()
        self.f_curve_angle.updateCanvas()
        self.f_curve_kParallel.updateCanvas()


    def place_widgets(self):
        self.f_curve_pixel.grid(row = 0, column= 0, sticky="news")
        self.f_curve_angle.grid(row = 1, column = 0, sticky="news")
        self.f_curve_kParallel.grid(row = 2, column = 0, sticky="news")
