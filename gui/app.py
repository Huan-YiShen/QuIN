import tkinter as tk
import frame as fm
from process.processCSV import *

footNote = "© QuIN Lab, 2024 Huan Yi Shen v0.1"

class App(tk.Tk):
    def __init__(self, 
                 title = "Curvature Detection",
                 size = (1024, 640)):
        # main setup
        super().__init__() # initiailze tk.Tk()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.config(background = "white")

        # initilizations
        self.initialize_variables()
        self.initialize_wigets() 
        self.variable_hook()

        self.widget_placement()
        self.mainloop()
    

    def initialize_variables(self):
        self.path = tk.StringVar() 
        self.wavelength_map = []        # row dhat indicate the wavelength of the spectrometer
        self.data = []                  # intensity value of a 2D array (transposed)
        # self.logMsg = tk.StringVar()  # TODO: change tb_logWindow to use StringVar


    def initialize_wigets(self):
        self.label_title = tk.Label(
            master = self, bg="light gray", height = 1,
            text = "Curvature Detection")
        self.label_footnote = tk.Label(
            master = self, bg="light gray", height = 1, anchor = "w", 
            text = footNote)

        self.f_fileSelect = fm.FrameFileSelection(self, self.path)
        self.f_imgFull = fm.FrameImageFull(self)
        self.f_imgCrop = fm.FrameImageCrop(self)


    def widget_placement(self):
        # self.F_fileSelect.place(x=0, y=0, relwidth = 1, relheight = 0.1)
        #Give the grid, column of the frame weight...

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.label_title.grid(column = 0, row = 0, columnspan = 2, sticky="ewn")
        self.f_fileSelect.grid(column = 0, row = 1, columnspan = 2, sticky="ewn")
        self.f_imgFull.grid(column = 0, row = 2, sticky="news")
        self.f_imgCrop.grid(column = 1, row = 2, sticky="news")
        self.label_footnote.grid(column = 0, row = 3, columnspan = 2, sticky="ews")


    def variable_hook(self):
        self.path.trace_add(
            "write", self.action_importData)


    def action_importData(self, *args):
        path = self.path.get()
        self.data = get_csv_data(path)
        self.wavelength_map = get_csv_wavelength(path)
        self.f_imgFull.update(path, self.data, self.wavelength_map)
        self.f_imgCrop.update(self.data, self.wavelength_map)

        


if __name__ == '__main__':
    App()