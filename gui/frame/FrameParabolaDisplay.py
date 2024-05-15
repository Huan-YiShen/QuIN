import tkinter as tk
from tkinter import ttk

from process.constants import square
from process.constants import pixel2angle_linear
from process.constants import angle2k_ll
from process.generatePlot import plot_parabola_overlay
from process.curvatureDetection import find_parabola
from frame.FrameCanvas import FrameCanvas
from frame.dataStruct import ParabolaData
from frame.dataStruct import Result

import numpy as np
import matplotlib.pyplot as plt


class FrameParabolaDisplay(tk.Frame):
    def __init__(self, parent, resData : ParabolaData):
        super().__init__(parent)
        self.fc_curve_pixel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.fc_curve_angle = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))
        self.fc_curve_kParallel = FrameCanvas(
            self, plt.figure(dpi = 100), size = (540, 320))

        self.data = resData

        # self.peak_fitting()
        self.place_widgets()


    def get_data(self):
        return self.data


    def update(self, max_index, max_eV, crop_index, parabola, parabolaVertex):
        parabolaVertex_x, parabolaVertex_y = parabolaVertex
        self.data.base_x_pixel = np.array(max_index)
        self.data.base_y_eV = np.array(max_eV)
        self.data.parabola_x_pixel = np.array(crop_index)
        self.data.parabola_y_eV = np.array(parabola)

        print("update FrameParabolaDisplay")
        plot_parabola_overlay(
            fig = self.fc_curve_pixel.fig, 
            base_x = self.data.base_x_pixel, 
            base_y = self.data.base_y_eV,
            parabola_x = self.data.parabola_x_pixel, 
            parabola = self.data.parabola_y_eV)
        
        self.data.base_x_angles = np.array(
            pixel2angle_linear(self.data.base_x_pixel, parabolaVertex_x))
        self.data.parabola_x_angles = np.array(
            pixel2angle_linear(self.data.parabola_x_pixel, parabolaVertex_x))


        # recalculate parabola for angle
        angles_popt = find_parabola(self.data.parabola_x_angles, self.data.parabola_y_eV)
        self.data.parabola_y_angles_eV = square(
            self.data.parabola_x_angles, angles_popt[0], angles_popt[1], angles_popt[2])

        plot_parabola_overlay(
            fig = self.fc_curve_angle.fig, 
            base_x = self.data.base_x_angles,
            base_y = self.data.base_y_eV,
            parabola_x = self.data.parabola_x_angles,
            parabola = self.data.parabola_y_angles_eV,
            x_label = "angle")
        
        # TODO currently hard coded to convert m to um 
        self.data.base_x_kpara = np.array(
            angle2k_ll(self.data.base_x_angles)*1e-6)
        self.data.parabola_x_kpara = np.array(
            angle2k_ll(self.data.parabola_x_angles)*1e-6)

        # recalculate parabola for angle
        kpara_popt = find_parabola(self.data.parabola_x_kpara, self.data.parabola_y_eV)
        self.data.parabola_y_kpara_eV = square(
            self.data.parabola_x_kpara, kpara_popt[0], kpara_popt[1], kpara_popt[2])

        plot_parabola_overlay(
            fig = self.fc_curve_kParallel.fig, 
            base_x = self.data.base_x_kpara,
            base_y = self.data.base_y_eV,
            parabola_x = self.data.parabola_x_kpara,
            parabola = self.data.parabola_y_kpara_eV,
            x_label = r'k$_{||} (\mu m^{-1}$)')

        self.fc_curve_pixel.updateCanvas()
        self.fc_curve_angle.updateCanvas()
        self.fc_curve_kParallel.updateCanvas()

        self.data.min_pixel_parabola = parabolaVertex_y
        self.data.min_angle_parabola = angles_popt[2]
        self.data.res = Result(kpara_popt[0])


    def place_widgets(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.fc_curve_pixel.grid(row = 0, column= 0, sticky="news")
        self.fc_curve_angle.grid(row = 0, column = 1, sticky="news")
        self.fc_curve_kParallel.grid(row = 0, column = 2, sticky="news")
