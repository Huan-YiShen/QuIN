import tkinter as tk
from tkinter import ttk

from gui_actions import *

class CurvatureDetection():
    def __init__(self):
        App()
    

# inherit object Tk() to class App 
class App(tk.Tk):
    def __init__(self, 
                 title = "Curvature Detection v2",
                 size = (900, 600)):
        # main setup
        super().__init__() # initiailze tk.Tk()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.config(background = "white")

        # initilizations
        self.initialize_variables()

        # widgets
        self.initialize_wigets()
        self.widget_placement()
        self.mainloop()
    

    def initialize_variables(self):
        self.wavelength_map = [] # row dhat indicate the wavelength of the spectrometer
        self.data = [] # intensity value of a 2D array (transposed)
        self.path = "" # file path TODO: not used now but should be used for save functions

        self.rawFig = plt.figure(dpi = 100)
        self.displayTrigRaw = tk.BooleanVar()
        self.curFig = plt.figure(dpi = 100)
        self.displayTrigCur = tk.BooleanVar()

        # self.logMsg = tk.StringVar() # TODO: change tb_logWindow to use StringVar


    def initialize_wigets(self):
        self.label_title = tk.Label(master = self, text = "curvature detection")
        self.tb_logWindow = tk.Text(self, height = 6, width = 96, wrap=NONE, bg = "ivory2")
        # TODO: change tb_logWindow to use StringVar
        self.F_fileSelect = Frame_FileSelection(
            self, self.rawFig, self.displayTrigRaw, self.tb_logWindow)
        self.F_canvasRaw = Frame_Canvas(
            self, self.rawFig, self.displayTrigRaw, self.tb_logWindow)
        self.F_detectPanel = Frame_DetectPanel(
            self, self.curFig, self.displayTrigCur, self.tb_logWindow)
        self.F_canvasCur = Frame_Canvas(
            self, self.curFig, self.displayTrigCur, self.tb_logWindow)
    
    def widget_placement(self):
        # self.F_fileSelect.place(x=0, y=0, relwidth = 1, relheight = 0.1)
        #Give the grid, column of the frame weight...
        Grid.rowconfigure(self, 0)
        Grid.columnconfigure(self, 0)

        row = 0
        col = 0
        colFullSpan = 3
        
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, minsize=200)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=3)

        # row 1
        self.label_title.grid(
            column = col, row = row, columnspan = colFullSpan, sticky="new")
        # row 2
        row += 1
        col = 0
        self.F_fileSelect.grid(
            column = col, row = row, columnspan = colFullSpan, sticky="new")
        # row 3
        row += 1
        col = 0
        self.F_canvasRaw.grid(column = col, row = row, sticky="news")
        col += 1
        self.F_detectPanel.grid(column = col, row = row, )
        col += 1
        self.F_canvasCur.grid(column = col, row = row, sticky="news")
        # row 3
        row += 1
        col = 0
        self.tb_logWindow.grid(
            column = col, row = row, columnspan= colFullSpan, sticky="news")    


# inherit from ttk.Frame 
class Frame_FileSelection(ttk.Frame):
    def __init__(self, parent, fig, displayTrigger, tb_logWindow):
        super().__init__(parent)
        self.rawFig = fig
        self.displayTrigger = displayTrigger
        self.tb_logWindow = tb_logWindow

        self.create_widgets()


    def create_widgets(self):
        label_file_explorer = tk.Label(self, text = "Select you files:")

        # scroll bar
        h = tk.Scrollbar(self, orient='horizontal')
        tb_fileSelect = tk.Text(self, height = 1, width = 84,  
                            wrap=tk.NONE, xscrollcommand=h.set)
        tb_fileSelect.insert(tk.INSERT, "C:/Users/James/Documents/UWaterloo/QuIN/QuIN - GitHub/imageAnalysis/labData/2023_11_15_Image Data-new_FW/2023_11_15_Image Data-new_FW/FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv") # for debug
        tb_fileSelect.see(tk.END)

        # selection buttons
        btn_fileGet = tk.Button(self, text = "≡",
                                command = lambda: action_selectFiles(tb_fileSelect))

        btn_fileSelect = tk.Button(self, text = "SELECT FILE", fg = "black", bg = "lemon chiffon",
                                command = lambda: action_getData(
                                    self.rawFig, self.displayTrigger, tb_fileSelect, self.tb_logWindow))

        ##########################################
        ################# layout #################
        ##########################################
        # create the grid
        # self.columnconfig()...
        self.grid_columnconfigure(1, weight=1)
        label_file_explorer.grid(row = 0, column = 0)
        tb_fileSelect.grid(row = 0, column = 1, sticky="e")
        btn_fileGet.grid(row = 0, column = 2)
        btn_fileSelect.grid(row = 0, column = 3)

        # place the widgets
        # label_file_explorer.place(x=0,y=0, relheight = 1, relwidth = 0.15)
        # tb_fileSelect.place(x=0,y=0, relheight = 1, relwidth = 0.8)
        # btn_fileGet.place(x=0,y=0, relheight = 1, relwidth = 0.05)
        # btn_fileSelect.place(x=0,y=0, relheight = 1, relwidth = 0.15)


class Frame_Canvas(tk.Frame):
    def __init__(self, parent, figure, updateBool, 
                 tb_logWindow, size = (350, 450)):
        super().__init__(
            parent, bg = "black", borderwidth = 2, 
            width = size[0], height = size[1])

        self.fig = figure
        self.updateFig = updateBool
        self.tb_logWindow = tb_logWindow # TODO: change this to use logMsg
        self.size = size
        updateBool.trace("w", self.updateCanvas)


    def updateCanvas(self, *args):
        self.tb_logWindow.insert(END, "LOG display generation...\n")

        # reset frame
        for widget in self.winfo_children():
            widget.destroy()
        # update canvas frame
        print(self.fig)
        # try:
        canvas = generate_canvas(self.fig, self)
        canvas.config(width = self.size[0], height = self.size[1]-50)
        canvas.pack(fill="both", expand=True)
        # except:
        #     self.tb_logWindow.config(fg = "red")
        #     self.tb_logWindow.insert(END, "ERR cannot update canvas\n")


        
class Frame_DetectPanel(ttk.Frame):
    def __init__(self, parent, fig, displayTrigger, tb_logWindow): ##### TODO: parameter need refactoring
        super().__init__(parent)
        self.figure = fig
        self.displayTrigger = displayTrigger
        self.tb_logWindow = tb_logWindow # TODO: change tb_logWindow to use StringVar
        self

        self.create_widgets()


    def create_widgets(self):
        btn_detect = tk.Button(self, text = "DETECT",
                            command = lambda: action_curveDetect(
                                self.figure, self.displayTrigger, self.tb_logWindow))
        
        ############################
        ########## layout ##########
        ############################
        btn_detect.grid(column = 0, row = 0)


if __name__ == '__main__':
    CurvatureDetection()