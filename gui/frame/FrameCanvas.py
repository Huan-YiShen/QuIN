import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class FrameCanvas(tk.Frame):
    def __init__(self, parent, figure, size = (300, 400)):
        super().__init__(
            parent, bg = "black", borderwidth = 2, 
            width = size[0], height = size[1])

        self.fig = figure
        self.size = size


    def updateCanvas(self):
        print("LOG display generation...\n")

        # reset frame
        for widget in self.winfo_children():
            widget.destroy()
        # update canvas frame
        print(self.fig)
        # try:
        canvas = self.generate_canvas()
        canvas.config(width = self.size[0], height = self.size[1])
        canvas.pack(fill="both", expand=True)
        # except:
        #     self.tb_logWindow.config(fg = "red")
        #     self.tb_logWindow.insert(END, "ERR cannot update canvas\n")


    def generate_canvas(self):
        # creating the Tkinter canvas, containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(self.fig, master = self)  
        canvas.draw()
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        return canvas.get_tk_widget()