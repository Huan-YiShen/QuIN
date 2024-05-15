from typing import Callable
import tkinter as tk
import pandas as pd
import re
import os
import matplotlib.figure

from frame.dataStruct import AnalysisFigures
from frame.dataStruct import ParabolaData
from process.constants import to_wl_nm

def split_path(file_path):
    try:
        directory, filename = os.path.split(file_path)
        return directory, filename
    except ValueError as e:
        print("Error when path:", e)
        return None, None


class LabelEntryBtn_save():
    def __init__(
            self, parent, titleText = "entry name", 
            varInitVal = "entry", btnText = " save ", var = None):
        
        if (var is None):
            self.var = tk.StringVar(value = varInitVal)
        else:
            self.var = var

        self.lb = tk.Label(parent, text = titleText)
        self.en = tk.Entry(parent, textvariable = self.var)
        self.btn = tk.Button(
            parent, text = btnText, borderwidth = 2)


    def get_label(self):
        return self.lb

    def get_entry(self):
        return self.en

    def get_btn(self):
        return self.btn

    def get_var(self):
        return self.var

    def get_entry_numbers(self):
        return [int(s) for s in re.findall(r'\d+', self.var.get())]


class FrameAnalysisResultSave(tk.Frame):
    def __init__(self, parent, data : ParabolaData, figures : AnalysisFigures):
        super().__init__(parent)
        self.data = data
        self.figures = figures
        self.create_widgets()


    def create_widgets(self):
        f_p = LabelEntryBtn_save(
            self, titleText = "save eV pixel graph", 
            varInitVal = r".\analysisResult\evVsPixel.png")
        f_a = LabelEntryBtn_save(
            self, titleText = "save eV angle graph", 
            varInitVal = r".\analysisResult\evVsAngle.png")
        f_k = LabelEntryBtn_save(
            self, titleText = "save eV K_|| graph", 
            varInitVal = r".\analysisResult\evVskparallel.png")
        f_res = LabelEntryBtn_save(
            self, titleText = "save data", 
            varInitVal = r".\analysisResult\data.csv")

        self.path_p_var = f_p.get_var()
        self.path_a_var = f_a.get_var()
        self.path_k_var = f_k.get_var()
        self.path_res_var = f_res.get_var()

        # widget placement
        f_p.get_label().grid(row=0, column=0, padx=20, sticky="w")
        f_a.get_label().grid(row=1, column=0, padx=20, sticky="w")
        f_k.get_label().grid(row=2, column=0, padx=20, sticky="w")
        f_res.get_label().grid(row=3, column=0, padx=20, sticky="w")
        
        f_p.get_entry().grid(row=0, column=1, sticky="news")
        f_a.get_entry().grid(row=1, column=1, sticky="news")
        f_k.get_entry().grid(row=2, column=1, sticky="news")
        f_res.get_entry().grid(row=3, column=1, sticky="news")

        f_p.get_btn().grid(row=0, column=1, sticky="e")
        f_a.get_btn().grid(row=1, column=1, sticky="e")
        f_k.get_btn().grid(row=2, column=1, sticky="e")
        f_res.get_btn().grid(row=3, column=1, sticky="e")

        # widget placement weight configureation
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.columnconfigure(0, weight = 0) # entry
        self.columnconfigure(1, weight = 1) # entry
        self.columnconfigure(2, weight = 0) # entry

        # link buttom function
        f_p.get_btn().config(command=lambda: self.save_fig(
            self.figures.pixel_ev, self.path_p_var.get()))
        f_a.get_btn().config(command=lambda: self.save_fig(
            self.figures.angle_ev, self.path_a_var.get()))
        f_k.get_btn().config(command=lambda: self.save_fig(
            self.figures.kpara_ev, self.path_k_var.get()))
        f_res.get_btn().config(command=lambda: self.save_data(
            self.path_res_var.get()))

        # self.btn_fileGet = tk.Button(
        #     self, text = "≡", borderwidth = 2, 
        #     command = lambda: self.action_save())


    def save_data(self, path : str):
        # check if path exist
        directory, file = split_path(path)
        if (directory is None or file is None): 
            pass

        if (not os.path.exists(directory)):
            os.mkdir(directory)

        filename, extension = os.path.splitext(file)
        if (extension is not ".csv"):
            print("ERR: data file must end with .csv")
            pass

        pathROI = directory + filename + "_ROI" + extension
        pathParabola = directory + filename + "_Parabola" + extension

        # store ROI
        max_index = self.data.base_x
        max_wl = to_wl_nm(self.data.base_y)
        max_eV = self.data.base_y
        angle = self.data.base_angles
        k_ll_um = self.data.base_kpara

        data_fitting_ROI = pd.DataFrame()
        data_fitting_ROI['pixel_ROI'] = max_index
        data_fitting_ROI['angle_ROI'] = angle
        data_fitting_ROI['k_ll_um_ROI'] = k_ll_um
        data_fitting_ROI['dispersion_ROI_nm'] = max_wl
        data_fitting_ROI['dispersion_ROI_eV'] = max_eV

        # SAVE #####
        data_fitting_ROI.to_csv(pathROI, index = False)
        # SAVE #####

        # fitting curve: Selected
        data_fitting_selec = pd.DataFrame()
        data_fitting_selec['pixel_selec'] = self.data.parabola_x
        data_fitting_selec['angle_selec'] = self.data.parabola_angles
        data_fitting_selec['k_ll_um_selec'] = self.data.parabola_kpara
        data_fitting_selec['dispersion_selec_nm'] = to_wl_nm(self.data.parabola_y)
        data_fitting_selec['dispersion_selec_eV'] = self.data.parabola_y
        # SAVE #####
        data_fitting_selec.to_csv(pathParabola, index = False)
        # SAVE #####

        # # fitting parameters
        # column_order = ['m_eff', 'm_eff_rel', 'min_wavelength (nm)', 'min_eV (eV)']
        # result = [m_eff, m_eff_rel, h*c/popt2[2]*1e9, popt3[2]]
        # result_collection = pd.DataFrame(result).T
        # result_collection.columns = column_order

        # result_collection.to_csv(path_csv_store + file[:-4]+'_' +str(wl_ini) +'-' + str(wl_las) +'nm' + '_result_Linear.csv', index = False)


    def save_fig(self, fig : matplotlib.figure.__class__, figPath : str = "unnamed_figure.jpg"):
        print("LOG: saving figure")
        directory, filename = split_path(figPath)
        if (not os.path.exists(directory)):
            os.mkdir(directory)

        fig.savefig(figPath)

