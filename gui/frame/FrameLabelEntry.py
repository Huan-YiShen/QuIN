import re
import tkinter as tk
from tkinter import ttk

'''
a frame class that contain entry with label (currently not used)
'''
class FrameLabelEntry(ttk.Frame):
    def __init__(
            self, parent, titleText = "entry name", 
            varDefaultVal = "[min, max]", var = None):

        super().__init__(parent)
        # self.config(width=500, height = 30)
        
        # set variable if given in initilization
        
        if (var is None):
            self.var = tk.StringVar(value = varDefaultVal)
        else:
            self.var = var
            
        self.lb = tk.Label(self, text = titleText)
        self.en = tk.Entry(self, textvariable = self.var)

        self.place_widget()


    def place_widget(self):
        self.lb.grid(row = 0, column = 0, padx=20, sticky="w")
        self.en.grid(row = 0, column = 1, sticky="news")
        # self.lb.place(relx = 0, rely = 0, relheight = 1.0, relwidth = 0.4)
        # self.en.place(relx = 0.4, rely = 0, relheight = 1.0, relwidth = 0.6)


    def get_frame(self):
        return self.frame


    def get_var(self):
        return self.var

    def get_entry_numbers(self):
        return [int(s) for s in re.findall(r'\d+', self.var.get())]