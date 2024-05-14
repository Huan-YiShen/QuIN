import tkinter as tk
from tkinter import ttk

import numpy as np

from frame.FrameParabolaDetect import FrameParabolaDetect
from frame.FrameParabolaDisplay import FrameParabolaDisplay
from frame.FrameAnalysisResultSave import FrameAnalysisResultSave
from frame.dataStruct import analysisFigures
from frame.dataStruct import parabolaData

TITLE = "Curvature Detection"
FOOT_NOTE = "© QuIN Lab, 2024 Huan Yi Shen v0.1"


'''
Analysis window
'''
class WindowAnalysis():

    def __init__(
        self, data : np.array.__class__ = np.array([]), 
        wl : np.array.__class__ = np.array([]), 
        pixelRange = (0,0), intensityRange = (0,0)):

        print(f'''LOG: creating analysis window
                data pixel count = {len(data)}
                wavelength length = {len(wl)}
                pixelRange = {pixelRange}
                intensityRange = {intensityRange}''')

        self.win = tk.Toplevel()

        self.win.title("Analysis")
        self.win.geometry('1600x750')
        self.win.minsize(1600, 760)

        self.win.title(TITLE)
        self.win.config(background="gray")

        self.data = data
        self.wl = wl
        self.pixelRange = pixelRange
        self.intensityRange = intensityRange

        self.resFigures = analysisFigures() # resulting figures
        self.resData = parabolaData() # resulting data

        self.generate_widgets()
        self.place_widgets()
        
        
    def close_win(self):
        self.win.destroy()


    def populate_figures(self):
        self.resFigures.init_fig = self.f_paraDetect.get_init_figure()
        self.resFigures.cropped_fig = self.f_paraDetect.get_fitting_figure()
        self.resFigures.pixel_ev = self.f_paraDisplay.fc_curve_pixel.fig
        self.resFigures.angle_ev = self.f_paraDisplay.fc_curve_pixel.fig
        self.resFigures.kpara_ev = self.f_paraDisplay.fc_curve_kParallel.fig        


    '''
        the control panel of in the analysis window
        contain methods like save image, etc
    '''
    def generate_controlFrame(self):
        f_control = ttk.Frame(self.win)

        f_title = ttk.Frame(f_control)
        lb_title = ttk.Label(f_title, text = "Analysis Control")
        btn_exit = ttk.Button(f_title, text = "EXIT", command = self.close_win)
        lb_title.grid(row = 0, column = 0, sticky = "w")
        btn_exit.grid(row = 0, column = 1, sticky = "e")

        lb_select = ttk.Label(f_control, text = "Analysis Control")
        
        # objective lens selection
        objectiveLensSelection = tk.IntVar()
        f_objectiveLens = ttk.Frame(f_control)
        rb_NA085 = ttk.Radiobutton(f_objectiveLens, text="NA0.85", variable=objectiveLensSelection, value=0)
        rb_NA042 = ttk.Radiobutton(f_objectiveLens, text="NA0.42", variable=objectiveLensSelection, value=1)
        rb_NA085.grid(row = 0, column = 0, sticky = "w")
        rb_NA042.grid(row = 0, column = 1, sticky = "w")

        # input focus of lenses
        inputFocus = tk.IntVar()
        f_inputFocus = ttk.Frame(f_control)
        rb_1 = ttk.Radiobutton(f_inputFocus, text="150mm", variable=inputFocus, value=0)
        rb_2 = ttk.Radiobutton(f_inputFocus, text="100mm", variable=inputFocus, value=1)
        rb_1.grid(row = 0, column = 0, sticky = "w")
        rb_2.grid(row = 0, column = 1, sticky = "w")


        f_title.grid(row = 0, column = 0)
        lb_select.grid(row = 1, column = 0)
        f_objectiveLens.grid(row = 2, column = 0)
        f_inputFocus.grid(row = 3, column = 0)
        return f_control


    def generate_widgets(self):
        self.label_footnote = tk.Label(
            master = self.win, bg="light gray", height = 1, anchor = "w", 
            text = FOOT_NOTE)

        self.f_control = self.generate_controlFrame()
        self.f_paraDisplay = FrameParabolaDisplay(self.win, self.resData)
        self.f_paraDetect = FrameParabolaDetect(
            self.win, self.data, self.wl, self.pixelRange[0], self.f_paraDisplay)
        
        self.populate_figures()
        
        self.f_result = FrameAnalysisResultSave(
            self.win, self.resData, self.resFigures)


    def place_widgets(self):
        self.win.rowconfigure(0, weight=1)
        self.win.rowconfigure(1, weight=1)
        self.win.columnconfigure(0, weight=1)
        self.win.columnconfigure(1, weight=1)

        self.f_control.grid(row = 0, column = 0, sticky="new")
        self.f_paraDetect.grid(row = 0, column = 1, sticky="news") # , padx = 10
        self.f_paraDisplay.grid(row = 1, column = 0, columnspan= 2, sticky="news")
        self.f_result.grid(row = 2, column = 0, columnspan= 2, sticky="ews") 
        self.label_footnote.grid(row = 3, column = 0, columnspan = 2, sticky="ews")