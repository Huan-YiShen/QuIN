import tkinter as tk
from tkinter import ttk

import numpy as np

from frame.FrameParabolaDetect import FrameParabolaDetect

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
        self.win.geometry('1200x600')
        
        self.data = data
        self.wl = wl
        self.pixelRange = pixelRange
        self.intensityRange = intensityRange

        self.generate_widgets()
        self.place_widgets()
        
        
    def close_win(self):
        self.win.destroy()


    '''
        the control panel of in the analysis window
        contain methods like save image, etc
    '''
    def generate_controlFrame(self):
        pass


    def generate_widgets(self):
        self.f_curvefit = FrameParabolaDetect(
            self.win, self.data, self.wl, self.pixelRange[0])
        self.f_control = self.generate_controlFrame()


    def place_widgets(self):
        ttk.Label(self.win, text = "A label").pack()
        ttk.Button(self.win, text = "EXIT", command = self.close_win).pack()
        self.f_curvefit.pack()