import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class FrameCanvas(tk.Frame):
    def __init__(self, parent, figure, size = (300, 400), toolBar = False):
        super().__init__(
            parent, bg = "black", borderwidth = 2, 
            width = size[0], height = size[1])

        self.fig = figure
        self.size = size
        self.toolBar = toolBar



    def updateCanvas(self, figure = None):
        print("LOG generating canvas ...")
        
        if figure is None:
            figure = self.fig

        # reset frame
        for widget in self.winfo_children():
            widget.destroy()

        print("\t", figure)
        try:
            canvas = self.generate_canvas(figure)
            canvas.config(width = self.size[0], height = self.size[1] + 10)
            canvas.pack(fill="both", expand=True)
        except Exception as e:
            print("ERR cannot update canvas")
            print(e)


    def generate_canvas(self, figure):
        # creating the Tkinter canvas, containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(figure, master = self)
        canvas.draw()

        # creating the Matplotlib toolbar
        if self.toolBar:
            toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=True)
            toolbar.update()
        # placing the toolbar on the Tkinter window

        return canvas.get_tk_widget()