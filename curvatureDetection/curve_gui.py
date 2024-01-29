import matplotlib.pyplot as plt
from findCurve import *

from tkinter import *
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


######################################
## global parameter ##################
######################################
WAVELENGTH_MAP = [] # row dhat indicate the wavelength of the spectrometer
DATA = [] # intensity value of a 2D array (transposed)
PATH = "" # file path
raw_data_fig = None

# layout
row = 1
col = 1
colFullSpan = 5

window = Tk()
tb_logWindow = Text(window, height = 5, width = 96, wrap=NONE, bg = "ivory2")
frame_canvas = Frame(window, bg="#ababab")


def action_selectFiles(textbox):
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("CSV Files","*.csv"),
                                                       ("all files", "*.*")))
    # Change label contents
    textbox.insert(INSERT, filename)
    textbox.see(END)
    PATH = filename


def action_importFile(textbox):
    inputFilePath = textbox.get("1.0", "end-1c")
    tb_logWindow.insert(END, "LOG open file: " + inputFilePath +"\n")

    global PATH, WAVELENGTH_MAP, DATA
    try:
       w, d = extractDataFromPixis(inputFilePath, tb_logWindow)
       # from this point onward, the global variables should not be changed
       PATH = inputFilePath 
       WAVELENGTH_MAP = w
       DATA = d
       tb_logWindow.insert(END, "LOG data extraction successful...\n")   
    except FileNotFoundError:
       tb_logWindow.config(fg = "red")
       tb_logWindow.insert(END, "ERR cannot find file \n")   
    # try:
    display_raw_figure()
    # except:
    #    tb_logWindow.config(fg = "red")
    #    tb_logWindow.insert(END, "ERR cannot display raw data \n")   

######################################
## canvas ############################
######################################
def generate_canvas(fig, frame):
    # creating the Tkinter canvas, containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = window)  
    canvas.draw()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
    toolbar.update()
    # placing the toolbar on the Tkinter window

    return canvas.get_tk_widget()
    

def display_raw_figure():
    global raw_data_fig
    tb_logWindow.insert(END, "LOG creating plot ...\n")
    print("DATA: ", DATA)
    print("WL: ", WAVELENGTH_MAP)
    raw_data_fig = plot_rawData(np.array(DATA), np.array(WAVELENGTH_MAP))
    tb_logWindow.insert(END, "LOG generating figure...\n")   
    can_rawData = generate_canvas(raw_data_fig, window) # TODO: frame_canvas

    can_rawData.configure(highlightbackground = "red")    
    can_rawData.grid(column = 1, row = 4, columnspan=2)
    

def display_detected_figure():
    pass
######################################
## MAIN ##############################
######################################
window.title('File Explorer')
window.geometry("900x500")
window.config(background = "white")


# widgets
label_title = Label(master = window, text = "curvature detection")
label_file_explorer = Label(window, text = "Select you files:")

h=Scrollbar(window, orient='horizontal')
tb_fileSelect = Text(window, height = 1, width = 84,  
                     wrap=NONE, xscrollcommand=h.set)
tb_fileSelect.insert(INSERT, "C:/Users/James/Documents/UWaterloo/QuIN/QuIN - GitHub/imageAnalysis/labData/2023_11_15_Image Data-new_FW/2023_11_15_Image Data-new_FW/FS-57_C-wave_575nm_30mW_900-1400nm_Slit100_full_Trans_1sec_2D.csv")
tb_fileSelect.see(END)


btn_fileGet = Button(window,
                        text = "≡",
                        command = lambda: action_selectFiles(tb_fileSelect))

btn_fileSelect = Button(window,
                        text = "SELECT FILE", fg = "black", bg = "lemon chiffon",
                        command = lambda: action_importFile(tb_fileSelect))


# row 1
label_title.grid(column = col, row = row, columnspan= colFullSpan)

# row 2
col = 1
row += 1
label_file_explorer.grid(column = col, row = row)
col += 1
tb_fileSelect.grid(column = col, row = row, columnspan=2)
col += 2
btn_fileGet.grid(column = col, row = row)
col += 1
btn_fileSelect.grid(column = col, row = row)

# row 3
col = 1
row += 1
tb_logWindow.grid(column = col, row = row, columnspan= colFullSpan)

# row 4

window.mainloop()